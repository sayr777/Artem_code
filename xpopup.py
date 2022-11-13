from kivy.properties import NumericProperty, BooleanProperty
from kivy.uix.popup import Popup

__author__ = 'ophermit'


class XPopup(Popup):
    """XPopup class. See module documentation for more information.
    """

    min_width = NumericProperty(None, allownone=True)
    '''Minimum width of the popup.
    :attr:`min_width` is a :class:`~kivy.properties.NumericProperty` and
    defaults to None.
    '''

    min_height = NumericProperty(None, allownone=True)
    '''Minimum height of the popup.
    :attr:`min_height` is a :class:`~kivy.properties.NumericProperty` and
    defaults to None.
    '''

    fit_to_window = BooleanProperty(False)
    '''This property determines if the pop-up larger than app window is
    automatically fit to app window.
    :attr:`fit_to_window` is a :class:`~kivy.properties.BooleanProperty` and
    defaults to False.
    '''

    def _norm_value(self, pn_value, pn_hint, pn_min, pn_max):
        """Normalizes one value
        :param pn_value: original value (width or height)
        :param pn_hint: original `size hint` (x or y)
        :param pn_min: minimum limit for the value
        :param pn_max: maximum limit for the value
        :return: tuple of normalized parameters (value, `size hint`)
        """
        norm_hint = pn_hint
        norm_value = pn_value

        if pn_min is not None and norm_value < pn_min:
            norm_value = pn_min
            norm_hint = pn_min / float(pn_max)

        if self.fit_to_window:
            if norm_value > pn_max:
                norm_value = pn_max
            if norm_hint is not None and norm_hint > 1:
                norm_hint = 1.

        return norm_value, norm_hint

    def _norm_size(self):
        """Applies the specified parameters
        """
        win_size = self.get_root_window().size[:]
        popup_size = self.size[:]

        norm_x = self._norm_value(popup_size[0], self.size_hint_x,
                                  self.min_width, win_size[0])
        norm_y = self._norm_value(popup_size[1], self.size_hint_y,
                                  self.min_height, win_size[1])
        self.width = norm_x[0]
        self.height = norm_y[0]
        self.size_hint = (norm_x[1], norm_y[1])

        # DON`T REMOVE OR FOUND AND FIX THE ISSUE
        # if `size_hint` is not specified we need to recalculate position
        # of the popup
        if (norm_x[1], norm_y[1]) == (None, None) and self.size != popup_size:
            self.property('size').dispatch(self)

    def open(self, *largs):
        super(XPopup, self).open(*largs)
        self._norm_size()
