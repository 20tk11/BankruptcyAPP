import numpy as np
import statsmodels.api as sm


class LogitModified(sm.Logit):
    def _deriv_mean_dparams(self, params):
        """
        Derivative of the expected endog with respect to the parameters.

        Parameters
        ----------
        params : ndarray
            parameter at which score is evaluated

        Returns
        -------
        The value of the derivative of the expected endog with respect
        to the parameter vector.
        """
        link = self.link()
        lin_pred = self.predict(params)
        idl = link.inverse_deriv(lin_pred)
        dmat = self.exog * idl[:, None]
        return dmat

    def link(self):
        from statsmodels.genmod.families import links
        link = links.Logit()
        return link

    def _deriv_score_obs_dendog(self, params):
        """derivative of score_obs w.r.t. endog

        Parameters
        ----------
        params : ndarray
            parameter at which score is evaluated

        Returns
        -------
        derivative : ndarray_2d
            The derivative of the score_obs with respect to endog. This
            can is given by `score_factor0[:, None] * exog` where
            `score_factor0` is the score_factor without the residual.
        """
        return self.exog

    def score_factor(self, params):
        """
        Logit model derivative of the log-likelihood with respect to linpred.

        Parameters
        ----------
        params : array_like
            The parameters of the model

        Returns
        -------
        score_factor : array_like
            The derivative of the loglikelihood for each observation evaluated
            at `params`.

        Notes
        -----
        .. math:: \\frac{\\partial\\ln L_{i}}{\\partial\\beta}=\\left(y_{i}-\\lambda_{i}\\right)

        for observations :math:`i=1,...,n`

        where the loglinear model is assumed

        .. math:: \\ln\\lambda_{i}=x_{i}\\beta
        """
        y = self.endog
        fitted = self.predict(params)
        return (y - fitted)

    def hessian_factor(self, params):
        """
        Logit model Hessian factor

        Parameters
        ----------
        params : array_like
            The parameters of the model

        Returns
        -------
        hess : ndarray, (nobs,)
            The Hessian factor, second derivative of loglikelihood function
            with respect to the linear predictor evaluated at `params`
        """
        L = self.predict(params)
        return -L * (1 - L)
        
    
