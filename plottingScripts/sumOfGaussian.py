import numpy as np
import matplotlib.pyplot as plt
import scipy.stats
import scipy.optimize

x = np.arange(-24.0,25.6,1.6)
ybasis=[1.1,1.01,1,0.9,0.8,0.6,0.45,0.35,0.3,0.29,0.25,0.22,0.2,0.18,0.17,0.16]
ybasis=[1.1,1.0,0.95,0.85,0.8,0.6,0.45,0.35,0.3,0.29,0.25,0.20,0.17,0.13,0.12,0.1]

yekstra=ybasis [::-1]
np.asarray(yekstra)
y=yekstra[:-1]+ybasis


def tri_norm(x, *args):
    s1, s2, k1,k2 = args
    ret = k1*scipy.stats.norm.pdf(x, loc=0,scale=s1)
    ret += k2*scipy.stats.norm.pdf(x, loc=0 ,scale=s2)
    return ret


params = [30, 5, 1, 1]

fitted_params,_ = scipy.optimize.curve_fit(tri_norm,x, y, p0=params)
print fitted_params


plt.plot(x, y, 'o')
xx = np.linspace(-55, 55, 1000)
plt.plot(xx,fitted_params[2]*scipy.stats.norm.pdf(xx,loc=0,scale=fitted_params[0])+fitted_params[3]*scipy.stats.norm.pdf(xx,loc=0,scale=fitted_params[1]))



#plt.plot(xx, tri_norm(xx, *fitted_params))
plt.show()





# def tri_norm(x, *args):
#     m1, m2, s1, s2, k1, k2 = args
#     ret = k1*scipy.stats.norm.pdf(x, loc=m1,scale=s1)
#     ret += k2*scipy.stats.norm.pdf(x, loc=m2 ,scale=s2)
#     return ret


# params = [1, 1, 1, 1, 1, 1]

# fitted_params,_ = scipy.optimize.curve_fit(tri_norm,x, y, p0=params)
# print fitted_params




# plt.plot(x, y, 'o')
# xx = np.linspace(-55, 55, 1000)
# plt.plot(xx, tri_norm(xx, *fitted_params))
# plt.show()
