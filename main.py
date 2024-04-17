import math
import alpha
import CoolProp.CoolProp as CP
from CoolProp.CoolProp import PropsSI

#Расчет выполнен по МУ2013 Н.Ю.Карапузовой - РАСЧЕТ ТЕПЛООБМЕННЫХ АППАРАТОВ
# Запроектировать вертикальный пароводяной подогреватель, предназна-
# ченный для подогрева воды системы отопления в цехах производственных
# помещений, при следующих условиях:

CP.set_config_string(CP.ALTERNATIVE_REFPROP_LIBRARY_PATH , 'C:\Program Files (x86)\REFPROP\REFPRP64.DLL')
print(CP.get_global_param_string("REFPROP_version"))
CP.set_config_bool(CP.REFPROP_USE_GERG , True)

dKC=273.15
composition = "REFPROP::Water"

# water
P_water = 0.148*10**6 #Pa
Tin_water = 21+dKC #K
Tout_water = 87+dKC #K
Vg_water = 213/3600 #m3|s

# heating vapor
P_vapor = 0.56*10**6 #Pa
Tin_vapor = 185+dKC #K
T_condensation = PropsSI('T','P',P_vapor,'Q',0,composition)
print("Температура конденсации пара", round(T_condensation-dKC,2),"°C")
Tout_vapor = T_condensation

#Определение тепловой нагрузки аппарата

Taverage_water = (Tin_water+Tout_water)/2
#Рассчитываю параметры для воды при средней температуре
Cp_water = PropsSI('CPMASS','P',P_water,'T',Taverage_water,composition)  # 	J/kg/K
Density_water = PropsSI('DMASS','P',P_water,'T',Taverage_water,composition)  # kg/m^3
Viscosity_water = PropsSI('VISCOSITY','P',P_water,'T',Taverage_water,composition) # Pa*s
VISkinem_water = Viscosity_water/Density_water
Conductivity_water = PropsSI('CONDUCTIVITY','P',P_water,'T',Taverage_water,composition) # W/m/K
Prandtl_water = PropsSI('Prandtl','P',P_water,'T',Taverage_water,composition) # W/m/K

Taverage_vapor = (Tin_vapor+Tout_vapor)/2
#Рассчитываю параметры для пара при средней температуре
Cp_vapor = PropsSI('CPMASS','P',P_vapor,'T',Taverage_vapor,composition)  # 	J/kg/K
Density_vapor = PropsSI('D','P',P_vapor,'T',Taverage_vapor,composition)  # kg/m^3
Viscosity_vapor = PropsSI('VISCOSITY','P',P_vapor,'T',Taverage_vapor,composition) # Pa*s
VISkinem_vapor = Viscosity_vapor/Density_vapor
Conductivity_vapor = PropsSI('CONDUCTIVITY','P',P_vapor,'T',Taverage_vapor,composition) # W/m/K
Prandtl_vapor = PropsSI('Prandtl','P',P_vapor,'T',Taverage_vapor,composition) # W/m/K
H_vapor  = PropsSI("H", "T", T_condensation, "Q", 1, composition)
H_liquid = PropsSI("H", "T", T_condensation, "Q", 0, composition)
dHvap    = H_vapor  -  H_liquid #J/kg

Q_water = Vg_water*Cp_water*Density_water*(Tout_water-Tin_water)
print("Тепловая нагрузка по воде", round(Q_water/1000,2),"кВт")

G_vapor = Q_water/(Cp_vapor*(Tin_vapor-Tout_vapor)+dHvap)  #kg/s
print("Массовый расход пара ",round(G_vapor,2)," кг/с")
Q1_vapor = Cp_vapor*G_vapor*(Tin_vapor-Tout_vapor)
Q2_vapor = dHvap*G_vapor
#Суммарное значение переданной теплоты паром воде
Q_vapor = Q2_vapor+Q1_vapor
print("Тепловая нагрузка по пару", round(Q_vapor/1000,2),"кВт")

#Расчет коэффициента теплопередачи и конструктивных размеров аппарата
d_tube = 0.038 #m
d_thickness = 0.001 #m
d_water = d_tube - 2*d_thickness
conductivity_tube = 39 #Wt/m/K
w_water = 1.8 #m/s
Re_water = d_water*w_water/VISkinem_water
print("Число Рейнольдса для трубного потока (вода) ", round(Re_water,2))
if Re_water>10**4:
    print("Режим течения в трубе - турбулентный")
else:
    print("Измените параметры, чтобы режим течения был турбулентным!")

alpha_water = alpha.inPipeMiheev(Re_water,Prandtl_water,Conductivity_water,d_water)
print("Коэффициент теплоотдачи от внутренней поверхности стенки трубки к водe ", round(alpha_water,2), "Вт/(м2 К)")

#Рассчитывают количество трубок в трубной решетке
n_tube = 4*Vg_water/(math.pi*d_water**2*w_water)
print("Расчетное количество трубок в трубной решетке ", math.ceil(n_tube))

# Принимаем ромбическое расположение труб в трубной решетке.
# По табл. 5 (прил. 2) находим действительное значение количества труб в ре-
# шетке n = 37 и относительный диаметр трубной решетки dтр/t = 6 Шаг между
# трубками диметром dнар = 38 мм равен t = 48 мм (прил. 2, табл. 6), тогда диаметр
# трубной решетки будет
n_tube = 37
dt_grid = 6
t_grid = 0.048
d_grid = dt_grid*t_grid
# Кольцевой зазор k между крайними трубками и корпусом принимаем
# равным 10 мм.
# Внутренний диаметр корпуса аппарата составит
clearance = 0.01
D_case = math.ceil((d_grid+2*clearance+d_tube)*10)/10
print("Внутренний диаметр корпуса аппарата",round(D_case,2),"м")
# Расчетное значение внутреннего диаметра кожуха округляют до ближай-
# шего размера: 400, 500, 600, 700, 800, 900, 1000, 1200, 1400, 1600, 1800, 2000,
# 2200, 2400, 2600, 2800, 3000, 3200, 3400, 3600, 3800, 4000 [7].
# При ромбическом расположении труб число шестиугольников для размещения труб определяется

m = math.sqrt(12*n_tube-3)/6-0.5

# Число труб по диагонали наибольшего шестиугольника составит
l = 2*m+1
# Общее число труб в шестиугольниках будет
n_tubes = 1+3*m+3*m**2

# Поверхность теплообмена в 1-й зоне. Определяют площадь межтрубного
# пространства для прохода пара
F_intertube = math.pi/4*(D_case**2-n_tubes*d_tube**2)
print("Площадь межтрубного пространтсва ", round(F_intertube,3), "m2")
# эквивалентный диаметр
Perimeter = math.pi*(D_case+n_tubes*d_tube)
d_eq = 4*F_intertube/Perimeter
# Скорость пара в межтрубном пространстве
w_vapor = G_vapor/F_intertube/Density_vapor

# Критерий Рейнольдса
Re_vapor = w_vapor*d_eq/VISkinem_vapor
print("Число Рейнольдса для межтрубного потока (пар) ", round(Re_vapor,2))
if Re_vapor>10**4:
    print("Режим течения - турбулентный")
else:
    print("Измените параметры, чтобы режим течения был турбулентным!")

alpha_vapor = alpha.inPipeMiheev(Re_vapor,Prandtl_vapor,Conductivity_vapor,d_eq)
print("Коэффициент теплоотдачи в межтрубном пространстве ", round(alpha_vapor,2), "Вт/(м2 К)")

# Коэффициент теплопередачи в 1-й зоне, Вт /(м2·°С)
R_poll = 0.00033 # м2 ·°С/Вт — термическое сопротивление накипи
HTC1 = 1/(1/alpha_water+d_thickness/conductivity_tube+1/alpha_vapor+R_poll)
print("Коэффициент теплопередачи в 1 зоне ", round(HTC1,2), "Вт/(м2 К)")

Tout_water1 = Tout_water - G_vapor*Cp_vapor*(Tin_vapor-Tout_vapor)/(Vg_water*Cp_water*Density_water)
print("Температура перед 1 зоной", round(Tout_water1-dKC,2),"°С")
#Температурный напор - Противоток
a = abs(Tin_vapor-Tout_water1)
b = abs(Tout_vapor-Tout_water)
if a>b:
    dT_more = a
    dT_less = b
else:
    dT_more = b
    dT_less = a

dTlog1 = (dT_more-dT_less)/math.log(dT_more/dT_less)

# Поверхность теплообмена 1-й зоны составит
F_vapor1 = Q1_vapor/HTC1/dTlog1
print("Поверхность теплообмена 1-й зоны составит", round(F_vapor1,2),"м2")

# Поверхность теплообмена во 2-й зоне. Предполагают, что во 2-й зоне ко-
# эффициент теплоотдачи от внутренней стенки трубки к жидкости равен ко-
# эффициенту теплоотдачи в 1-й зоне. Это допустимо, так как свойства воды во
# 2-й зоне мало отличаются от свойств воды в 1-й зоне.

Conductivity_vapor_cond = PropsSI("CONDUCTIVITY","P",P_vapor,"T",T_condensation,composition)
Density_vapor_cond = PropsSI("D","P",P_vapor,"T",T_condensation,composition)
Viscosity_vapor_cond = PropsSI("VISCOSITY","P",P_vapor,"T",T_condensation,composition)
VISkinem_vapor_cond = Viscosity_vapor_cond/Density_vapor_cond
# Скорость жидкости в межтрубном пространстве

w_vapor_cond = G_vapor/F_intertube/Density_vapor_cond
Re_vapor_cond = w_vapor_cond*d_eq/VISkinem_vapor_cond

print("Число Рейнольдса для межтрубного потока (конденсация) ", round(Re_vapor_cond,2))
if Re_vapor_cond>10**4:
    print("Режим течения - турбулентный")
    if Re_vapor_cond<10**3:
        print("Режим течения - ламинарный")
else:
    print("Проверьте параметры потока")

#Температурный напор 2 зоны - Противоток
a = abs(Tout_vapor-Tout_water1)
b = abs(Tout_vapor-Tin_water)
if a>b:
    dT_more = a
    dT_less = b
else:
    dT_more = b
    dT_less = a

dTlog2 = (dT_more-dT_less)/math.log(dT_more/dT_less)

# Местный и средний коэффициенты теплоотдачи при ламинар-
# ном течении пленки конденсата на вертикальной плоской стенке или
# вертикальной трубе (формулы Нуссельта)
alpha_vapor2 = (Conductivity_vapor_cond**3*dHvap*(Density_vapor_cond-Density_vapor)*9.81/4/VISkinem_vapor_cond/dTlog2)**(1/4)

print("Коэффициент теплоотдачи в межтрубном пространстве при конденсации ", round(alpha_vapor2,2), "Вт/(м2 К)")

# Коэффициент теплопередачи в 2-й зоне, Вт /(м2·°С)
R_poll = 0.00033 # м2 ·°С/Вт — термическое сопротивление накипи
HTC2 = 1/(1/alpha_water+d_thickness/conductivity_tube+1/alpha_vapor2+R_poll)
print("Коэффициент теплопередачи в 2 зоне ", round(HTC2,2), "Вт/(м2 К)")

# Поверхность теплообмена во 2-й зоне, м2
F_vapor2 = Q2_vapor/HTC2/dTlog2
print("Поверхность теплообмена 2-й зоны составит", round(F_vapor2,2),"м2")

# Суммарная поверхность теплообмена, м2
F_vapor = F_vapor1+F_vapor2
print("Поверхность теплообмена суммарная", round(F_vapor,2),"м2")

# Общая длина трубок, м
d_average = (d_tube+d_water)/2 # средний диаметр трубок
L_tubes = F_vapor/math.pi/d_average/n_tubes
print("Общая длина трубок ",round(L_tubes,2),"м")

# Число ходов подогревателя
h_tube = 9  #предполагаемая высота трубок (hтр =1; 1,5; 2; 3; 4; 6; 9 м);
Z = math.ceil(L_tubes/h_tube)
print("Принимаем", Z,"-ходовой подогреватель.")
# Общее число трубок подогревателя составит
N_tubes = n_tubes*Z

# Для определения диаметра корпуса необходимо пересчитать размеры
# трубной решетки. Поскольку аппарат четырехходовой, необходимо предусмотреть
# место для перегородок и анкерных связей и в каждом ходе разместить по 37 трубок.
# Принимаем ромбическое расположение труб в трубной решетке. По табл. 5
# (прил. 2) находим действительное значение количества труб в решетке n = 187
N_tubes = 187
# и относительный диаметр трубной решетки dтр/t = 14 Шаг между трубками
# диаметром dнар = 38 мм равен t = 48 мм (прил. 2, табл. 6), тогда диаметр трубной решетки будет

dt_grid = 14
t_grid = 0.048
d_grid = dt_grid*t_grid
# Кольцевой зазор k между крайними трубками и корпусом принимаем равным 10 мм.
# Внутренний диаметр корпуса аппарата составит
clearance = 0.01
D_case = math.ceil((d_grid+2*clearance+d_tube)*10)/10 #округляем до ближайшего из ряда
print("Внутренний диаметр корпуса аппарата",round(D_case,2),"м")
# Внутренний диаметр многоходового теплообменника определяют с учетом
# размещения перегородок в распределительной камере и руководствуются
# рекомендациями [7]. Принимаем Dа.вн = 800 мм.
# Определяют площадь межтрубного пространства без учета перегородок для
# прохода пара, м2
F_intertube = math.pi/4*(D_case**2-N_tubes*d_tube**2)
print("Площадь межтрубного пространства", round(F_intertube,2),"м2")

# Коэффициент, учитывающий сужение живого сечения межтрубного пространства
pfi = (1-d_tube/t_grid)/(1-0.9*(d_tube/t_grid)**2) # стоит проверить формулу (!!0.9!!)

# Расстояние между сегментными перегородками, м
l_segment = F_intertube/D_case/(1-d_tube/t_grid)

# Эквивалентная длина пути теплоносителя, м
b_dist = D_case*(0.2) #расстояние от края сегментной перегородки до корпуса аппарата - коэффициент 0.2%0.4
L_eq = l_segment+D_case-4/3*b_dist
# Площадь живого сечения межтрубного пространства с учетом перегородок
F_sech = F_intertube * l_segment*pfi/L_eq
print("Площадь живого сечения межтрубного пространства с учетом перегородок",round(F_sech,2),"м2")
# Скорость пара в межтрубном пространстве
w_vapor =G_vapor/F_sech/Density_vapor
print("Скорость пара в межтрубном пространстве",round(w_vapor,2),"м/с")
Perimeter = math.pi*(D_case+N_tubes*d_tube)
d_eq = 4*F_sech/Perimeter
Re_vapor = w_vapor*d_eq/VISkinem_vapor

print("Число Рейнольдса для межтрубного потока (пар) ", round(Re_vapor,2))
if Re_vapor>10**4:
    print("Режим течения - турбулентный")
else:
    print("Измените параметры, чтобы режим течения был турбулентным!")

alpha_vapor = alpha.inPipeMiheev(Re_vapor,Prandtl_vapor,Conductivity_vapor,d_eq)
print("Коэффициент теплоотдачи в межтрубном пространстве ", round(alpha_vapor,2), "Вт/(м2 К)")
# Коэффициент теплопередачи в 1-й зоне, Вт /(м2·°С)
R_poll = 0.00033 # м2 ·°С/Вт — термическое сопротивление накипи
HTC1 = 1/(1/alpha_water+d_thickness/conductivity_tube+1/alpha_vapor+R_poll)
print("Коэффициент теплопередачи в 1 зоне ", round(HTC1,2), "Вт/(м2 К)")
# Считаем, что температурный напор в 1-й зоне не изменится
F_vapor1 = Q1_vapor/HTC1/dTlog1
print("Поверхность теплообмена 1-й зоны составит", round(F_vapor1,2),"м2")

# Так как температурный напор во 2-й зоне не изменяется, то
# коэффициент теплопередачи останется прежним
# а следовательно, поверхность теплообмена также не изменится
# Суммарная поверхность теплообмена, м2
F_vapor = F_vapor1+F_vapor2
print("Поверхность теплообмена суммарная", round(F_vapor,2),"м2")

# Длина трубок, м, в одном ходу
h_tube = F_vapor/math.pi/d_average/N_tubes
print("Длина трубок в одном ходу",round(h_tube,2),"м")

# Принимаем четырехходовой подогреватель с внутренним диаметром кожуха Dа.вн = 800 мм,
# диаметром трубок d = 38×2, длиной трубок hтр = 6,9 м, поверхностью теплообмена F = 150,5 м2,
# площадью проходного сечения в трубном пространстве f = 0,15 м2т.п
# , в межтрубном — fпр = 0,1 м2 [7].