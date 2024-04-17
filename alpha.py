import math

def interPipe(Re_m,Pr_m,conductivity_m,d_m):
    NU_m = 0.27 * Re_m ** 0.63 * Pr_m ** 0.36
    alpha_m = NU_m * conductivity_m / d_m  # коэффициент теплоотдачи в межтрубном пространстве
    return alpha_m

def inPipeMiheevCurve(Re_t,Pr_t,conductivity_t,d_t, R_izg):
    NU_t = 0.021 * Re_t ** 0.8 * Pr_t ** 0.43 * (1 + 1.77 * d_t / R_izg)
    alpha_t = NU_t * conductivity_t / d_t  # коэффициент теплоотдачи в трубном пространстве
    return alpha_t

def inPipeMiheev(Re_t,Pr_t,conductivity_t,d_t):
    NU_t = 0.021 * Re_t ** 0.8 * Pr_t ** 0.43
    alpha_t = NU_t * conductivity_t / d_t  # коэффициент теплоотдачи в трубном пространстве
    return alpha_t


def kHeat(alpha_m,alpha_t,d_n,d_t,t,conductivity,z1,z2):
    k = 1 / (1 / alpha_m + (1 / alpha_t) * (d_n / d_t) + t / conductivity + z1 + z2)
    return k