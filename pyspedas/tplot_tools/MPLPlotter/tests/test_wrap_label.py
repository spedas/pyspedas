"""Unit tests for the ``wrap_label`` helper used by ``tplot`` when ``xwrap``
or ``ywrap`` is enabled (issue #1444).

The helper wraps axis titles so long labels do not overflow the panel. We test
it in isolation because it is a pure string transform (no matplotlib state),
which is faster and more deterministic than asserting on rendered axes.

The helper lives in :mod:`pyspedas.tplot_tools.MPLPlotter.label_wrap` (kept
dependency-free) so this test does not need matplotlib or the full
``pyspedas`` package init chain.
"""
import unittest

from pyspedas.tplot_tools.MPLPlotter.label_wrap import wrap_label, _wrap_label


class TestWrapLabel(unittest.TestCase):
    """Behavioural contract for ``_wrap_label``."""

    # --- Passthrough cases ------------------------------------------------

    def test_empty_string_returns_empty(self):
        self.assertEqual(_wrap_label(""), "")

    def test_short_label_returns_unchanged(self):
        self.assertEqual(_wrap_label("Energy (eV)"), "Energy (eV)")

    def test_label_fitting_within_width_returns_unchanged(self):
        # 40 chars exactly; should not wrap
        label = "a" * 40
        self.assertEqual(_wrap_label(label), label)

    # --- Wrapping cases ---------------------------------------------------

    def test_long_label_wraps_on_whitespace(self):
        long_label = (
            "Differential Energy Flux (cm^-2 s^-1 sr^-1 keV^-1) "
            "for the MMS FPI instrument"
        )
        out = _wrap_label(long_label, width=40)
        # Every wrapped line must be <= width chars
        for line in out.split("\n"):
            self.assertLessEqual(len(line), 40)
        # Total content (whitespace-collapsed) must round-trip
        self.assertEqual(out.replace("\n", " ").split(), long_label.split())

    def test_wrap_default_width_is_40(self):
        # Construct a label just over 40 chars with a wrap point at 41
        long_label = "word " * 10  # 50 chars
        out = _wrap_label(long_label)
        for line in out.split("\n"):
            self.assertLessEqual(len(line), 40)

    def test_wrap_preserves_scientific_notation(self):
        # break_long_words=False must NOT split "1e-6" mid-token
        label = "electron density 1e-6 cm^-3 proton flux 1e-3 /cm2/s"
        out = _wrap_label(label, width=20)
        # No line may split a token
        for line in out.split("\n"):
            self.assertNotIn("1e\n", line)
            self.assertNotIn("cm\n", line)
        # Tokens must round-trip
        self.assertEqual(out.replace("\n", " ").split(), label.split())

    def test_wrap_preserves_hyphenated_units(self):
        # break_on_hyphens=False must NOT split "m/s^2" mid-hyphen
        label = "Velocity m/s^2 along the GSE-X axis direction"
        out = _wrap_label(label, width=20)
        self.assertNotIn("m/s\n", out)
        self.assertNotIn("^\n", out)

    def test_wrap_preserves_underscored_names(self):
        # Subscripts like x_1, n_e must not be split
        label = "n_e measurement from mms_fpi_dis_dist"
        out = _wrap_label(label, width=20)
        self.assertNotIn("_\n", out)
        self.assertNotIn("n\n", out)

    # --- Newline preservation --------------------------------------------

    def test_embedded_newlines_preserved_as_hard_breaks(self):
        # The combined ytitle + '\n' + ysubtitle pattern from tplot()
        combined = "ytitle line\nysubtitle line"
        out = _wrap_label(combined, width=80)
        # Both lines present, joined by newline
        self.assertIn("ytitle line", out)
        self.assertIn("ysubtitle line", out)
        # No line exceeds width (both are short here)
        for line in out.split("\n"):
            self.assertLessEqual(len(line), 80)

    def test_each_newline_segment_wraps_independently(self):
        combined = (
            "A very long ytitle that exceeds forty characters on purpose\n"
            "short subtitle"
        )
        out = _wrap_label(combined, width=40)
        lines = out.split("\n")
        # First segment should wrap (was > 40 chars); second stays single
        self.assertGreater(len(lines), 2)
        for line in lines:
            self.assertLessEqual(len(line), 40)

    # --- Width boundary --------------------------------------------------

    def test_custom_width_respected(self):
        label = "alpha beta gamma delta epsilon zeta eta theta"
        out = _wrap_label(label, width=15)
        for line in out.split("\n"):
            self.assertLessEqual(len(line), 15)


if __name__ == "__main__":
    unittest.main()
