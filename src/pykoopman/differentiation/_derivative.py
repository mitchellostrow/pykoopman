"""Wrapper classes for differentiation methods from the :doc:`derivative:index` package.

Some default values used here may differ from those used in :doc:`derivative:index`.
"""
from __future__ import annotations

from derivative import dxdt
from numpy import arange
from sklearn.base import BaseEstimator

from ..common import validate_input


class Derivative(BaseEstimator):
    """
    Wrapper class for differentiation classes from the :doc:`derivative:index` package.
    This class is meant to provide all the same functionality as the
    `dxdt <https://derivative.readthedocs.io/en/latest/api.html\
        #derivative.differentiation.dxdt>`_ method.

    This class includes a :meth:`__call__` method.

    Parameters
    ----------
    derivative_kws: dictionary, optional
        Keyword arguments to be passed to the
        `dxdt <https://derivative.readthedocs.io/en/latest/api.html\
        #derivative.differentiation.dxdt>`_
        method.

    Notes
    -----
    See the `derivative documentation <https://derivative.readthedocs.io/en/latest/>`_
    for acceptable keywords.
    """

    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def set_params(self, **params):
        """
        Set the parameters of this estimator.

        Returns
        -------
        self
        """
        if not params:
            # Simple optimization to gain speed (inspect is slow)
            return self
        else:
            self.kwargs.update(params)

        return self

    def get_params(self, deep=True):
        """Get parameters."""
        params = super().get_params(deep)

        if isinstance(self.kwargs, dict):
            params.update(self.kwargs)

        return params

    def __call__(self, x, t, axis=0):
        """
        Perform numerical differentiation by calling the ``dxdt`` method.

        Paramters
        ---------
        x: np.ndarray, shape (n_samples, n_features)
            Data to be differentiated. Rows should correspond to different
            points in time and columns to different features.

        t: np.ndarray, shape (n_samples, )
            Time points for each sample (row) in ``x``.

        Returns
        -------
        x_dot: np.ndarray, shape (n_samples, n_features)
        """
        x = validate_input(x, t=t)

        if isinstance(t, (int, float)):
            if t < 0:
                raise ValueError("t must be a positive constant or an array")
            t = arange(x.shape[0]) * t

        return dxdt(x, t, axis=axis, **self.kwargs)
