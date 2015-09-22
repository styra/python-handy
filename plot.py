import numpy as np
import matplotlib.pyplot as plt

__all__ = ['mid', 'circles', 'compare']

def mid(x):
  x = np.asarray(x)
  return (x[1:] + x[:-1])/2.

def circles(x, y, s, c='b', ax=None, vmin=None, vmax=None, **kwargs):
    """
    Make a scatter of circles plot of x vs y, where x and y are sequence 
      like objects of the same lengths. The size of circles are in data scale.

    Parameters
    ----------
    x,y : scalar or array_like, shape (n, )
        Input data
    s : scalar or array_like, shape (n, ) 
        Radius of circle in data scale (ie. in data unit)
    c : color or sequence of color, optional, default : 'b'
        `c` can be a single color format string, or a sequence of color
        specifications of length `N`, or a sequence of `N` numbers to be
        mapped to colors using the `cmap` and `norm` specified via kwargs.
        Note that `c` should not be a single numeric RGB or
        RGBA sequence because that is indistinguishable from an array of
        values to be colormapped.  `c` can be a 2-D array in which the
        rows are RGB or RGBA, however.
    ax : Axes object, optional, default: None
        Parent axes of the plot. It uses gca() if not specified.
    vmin, vmax : scalar, optional, default: None
        `vmin` and `vmax` are used in conjunction with `norm` to normalize
        luminance data.  If either are `None`, the min and max of the
        color array is used.  (Note if you pass a `norm` instance, your
        settings for `vmin` and `vmax` will be ignored.)

    Returns
    -------
    paths : `~matplotlib.collections.PathCollection`

    Other parameters
    ----------------
    kwargs : `~matplotlib.collections.Collection` properties
        eg. alpha, edgecolors, facecolors, linewidths, linestyles, norm, cmap

    Examples
    --------
    a = np.arange(11)
    circles(a, a, a*0.2, c=a, alpha=0.5, edgecolor='none')

    License
    --------
    This code is under [The BSD 3-Clause License]
    (http://opensource.org/licenses/BSD-3-Clause)
    """
    from matplotlib.patches import Circle
    from matplotlib.collections import PatchCollection

    if ax is None:
        ax = plt.gca()

    if isinstance(c,basestring):
        color = c     # ie. use colors.colorConverter.to_rgba_array(c)
    else:
        color = None  # use cmap, norm after collection is created
    kwargs.update(color=color)

    if np.isscalar(x):
        patches = [Circle((x, y), s),]
    elif np.isscalar(s):
        patches = [Circle((x_,y_), s) for x_,y_ in zip(x,y)]
    else:
        patches = [Circle((x_,y_), s_) for x_,y_,s_ in zip(x,y,s)]
    collection = PatchCollection(patches, **kwargs)

    if color is None:
        collection.set_array(np.asarray(c))
        if vmin is not None or vmax is not None:
            collection.set_clim(vmin, vmax)

    ax.add_collection(collection)
    ax.autoscale_view()
    
    return collection
    
def compare(x, y, xbins=None, ybins=None, 
             ax=None, ls=None, nan=None, 
             xlim=None, ylim=None, xlabel=None, ylabel=None,
             line=True, point=True, fill=False, 
             xref=None, yref=None, xref_label=None, yref_label=None, 
             legend=False, loc=1, frameon=True):
    if xbins is not None:
        w, z, bins = x, y, xbins
    elif ybins is not None:
        w, z, bins = y, x, ybins
    else:
        xbins = linspace(np.nanmin(x), np.nanmax(x), 11)
        w, z, bins = x, y, xbins
                        
    nbins = len(bins) - 1
    zs = np.full((5,nbins), np.nan)
           
    ps = [50, 15.8, 84.2, 2.3, 97.7]
    idx = np.isnan(z)
    if nan is None:
        z, w = z[~idx], w[~idx]
    else:
        z = z.copy().astype('f')
        z[idx] = nan
    for i in range(nbins):
        zc = z[(w > bins[i]) * (w < bins[i+1])]
        nc = len(zc)
        if nc >= 120:
            zs[:5, i] = np.percentile(zc, ps[:5])
        elif nc >= 20:
            zs[:3, i] = np.percentile(zc, ps[:3])
        elif nc >= 8:
            zs[:1, i] = np.percentile(zc, ps[:1])
    w0 = (bins[:-1] + bins[1:])/2.

    if ax is not None:
        plt.sca(ax)
    else:
        ax = plt.gca()
        
    if xbins is not None:
        xs, ys = [w0, w0, w0, w0, w0], zs
        fill_between = ax.fill_between
    else:
        xs, ys = zs, [w0, w0, w0, w0, w0]
        fill_between = ax.fill_betweenx

    if line:
        ls = ls if ls else ['k-', 'b--', 'g:']
        ax.plot(xs[0], ys[0], ls[0], label='median'  if legend else None)
        ax.plot(xs[1], ys[1], ls[1], label='1 sigma' if legend else None)
        ax.plot(xs[2], ys[2], ls[1])
        ax.plot(xs[3], ys[3], ls[2], label='2 sigma' if legend else None)
        ax.plot(xs[4], ys[4], ls[2])     
    if point:
        ax.scatter(xs[0], ys[0], s=2)
    if fill:
        fill_between(w0, zs[1], zs[2], color=ls[1][0], alpha=0.3)
        fill_between(w0, zs[3], zs[4], color=ls[2][0], alpha=0.2)
    
    if xlabel is not None:
        ax.set_xlabel(xlabel)
    if ylabel is not None:
        ax.set_ylabel(ylabel)
    if yref is not None:
        ax.axhline(yref, color='r',alpha=0.6, ls='--', label=yref_label)
    if xref is not None:
        ax.axvline(xref, color='m',alpha=0.6, ls='--', label=xref_label)
    if xlim is not None:
        ax.set_xlim(xlim)
    if ylim is not None:
        ax.set_ylim(ylim)
    if legend:
        ax.legend(loc=loc, frameon=frameon)
    plt.draw()
    
    #return xs[0], ys[0]
    return w0, zs
