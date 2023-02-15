class MLEInfluence(_BaseInfluenceMixin):
    @cache_readonly
    def _get_prediction(self):
        # TODO: do we cache this or does it need to be a method
        # we only need unchanging parts, alpha for confint could change
        covb = self.cov_params
        var_pred_mean = (self.exog * np.dot(covb, self.exog.T).T).sum(1)
        return np.sqrt(var_pred_mean)