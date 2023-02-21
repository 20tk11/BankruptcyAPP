import math
import pandas as pd
import statsmodels.api as sm
import numpy as np

linearData = pd.DataFrame()
linearData["x"] = [3.78, 2.44, 2.09, 0.14, 1.72,
                   1.65, 4.92, 4.37, 4.96, 4.52, 3.69, 5.88]
linearData["z"] = [1.56, 3.44, 8.09, 1.14, 0.72,
                   3.65, 1.92, 0.37, 6.96, 1.52, 0.69, 2.88]
linearData["c"] = [3.78, 2.44, 2.09, 0.14, 1.72,
                   1.23, 4.01, 4.00, 4.31, 4.02, 3.54, 5.85]
linearData["y"] = [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1]


exog = sm.add_constant(linearData[["x", "z", "c"]])
rownames = linearData.dropna().index
model = sm.Logit(linearData["y"], exog, missing='drop')
fittedModel = model.fit(disp=0, method="bfgs")
print(fittedModel.normalized_cov_params)
print(np.diag(fittedModel.normalized_cov_params))

# print(fittedModel.get_influence().summary_frame())

# exog = sm.add_constant(linearData["x"])
# mod = sm.Logit(linearData["y"], exog, missing='drop')
# res = mod.fit()
# print(res.summary())

# denumerator = math.sqrt(res1.mse_resid*np.diag(res.normalized_cov_params)[0])
# print("mse resid")
# print(res1.mse_resid)
# print("unscaled cov")
# print(np.diag(res.normalized_cov_params)[0])
# print("result")
# print(numerator/denumerator)
# print(res1.resid)
# print(res1.params[0])
# print(res1.params[1])

# residuals = (np.array([0.545, -0.02, -0.137, -0.751]) - predictions)**2
# print(predictions)
# print(residuals)
# print(residuals[1])
# print(res1.nobs)
# mse_resid = 0
# for i in residuals:
#     print(i)
#     mse_resid = mse_resid + i
# print(mse_resid)
# print(mse_resid/2)
# print(res1.summary())


# getDFbetas(mod, res, rownames)
