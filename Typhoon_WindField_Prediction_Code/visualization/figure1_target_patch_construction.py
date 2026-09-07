"""Draw a schematic of the corrected fixed-t0 target construction.

The diagram is intentionally schematic: all trajectory positions and patch
windows are illustrative.  It documents the construction used by the data
pipeline, not a particular storm or geographical domain.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch, Rectangle


BLUE = "#2A6F9E"
GREEN = "#2C8C66"
RED = "#C95B50"
ORANGE = "#C98045"
DARK = "#202020"
GRAY = "#6E747B"
LIGHT_GRAY = "#D7DCE0"


def add_panel_frame(axis: plt.Axes, title: str, accent: str) -> None:
    """Set up a clean publication-style panel with a subtle colored header rule."""
    axis.set_xlim(0, 1)
    axis.set_ylim(0, 1)
    axis.set_axis_off()
    axis.add_patch(
        FancyBboxPatch(
            (0.012, 0.012),
            0.976,
            0.976,
            boxstyle="round,pad=0.006,rounding_size=0.010",
            facecolor="white",
            edgecolor="#B9C0C5",
            linewidth=0.85,
            transform=axis.transAxes,
            zorder=0,
        )
    )
    axis.plot((0.045, 0.955), (0.908, 0.908), color=accent, linewidth=1.45, solid_capstyle="butt", zorder=1)
    axis.text(0.05, 0.945, title, ha="left", va="center", fontsize=13.2, fontweight="bold", color=DARK)


def add_storm_center(axis: plt.Axes, x: float, y: float, color: str, label: str, *, label_side: str = "above") -> None:
    """Draw a storm-center marker and a compact mathematical label."""
    axis.add_patch(Circle((x, y), 0.014, facecolor=color, edgecolor="white", linewidth=0.7, zorder=6))
    offset = 0.038 if label_side == "above" else -0.042
    va = "bottom" if label_side == "above" else "top"
    axis.text(x, y + offset, label, ha="center", va=va, fontsize=9.1, color=DARK, zorder=7)


def add_patch_window(
    axis: plt.Axes,
    center: tuple[float, float],
    size: float,
    color: str,
    label: str,
    *,
    alpha: float = 0.10,
    label_position: str = "below",
) -> None:
    """Draw a regular-grid 31 x 31 patch-window schematic around ``center``."""
    x, y = center
    lower_left = (x - size / 2, y - size / 2)
    axis.add_patch(
        Rectangle(
            lower_left,
            size,
            size,
            facecolor=color,
            edgecolor=color,
            linewidth=1.55,
            alpha=alpha,
            zorder=2,
        )
    )
    # A sparse regular lattice denotes the full 31 x 31 grid without turning
    # a small explanatory panel into a visually dense raster.
    for fraction in (1 / 6, 2 / 6, 3 / 6, 4 / 6, 5 / 6):
        axis.plot(
            (lower_left[0] + size * fraction, lower_left[0] + size * fraction),
            (lower_left[1], lower_left[1] + size),
            color=color,
            linewidth=0.42,
            alpha=0.63,
            zorder=3,
        )
        axis.plot(
            (lower_left[0], lower_left[0] + size),
            (lower_left[1] + size * fraction, lower_left[1] + size * fraction),
            color=color,
            linewidth=0.42,
            alpha=0.63,
            zorder=3,
        )
    axis.add_patch(Circle(center, 0.008, facecolor=color, edgecolor="white", linewidth=0.4, zorder=5))
    label_y = lower_left[1] - 0.026 if label_position == "below" else lower_left[1] + size + 0.025
    vertical_alignment = "top" if label_position == "below" else "bottom"
    axis.text(x, label_y, label, ha="center", va=vertical_alignment, fontsize=8.1, color=color, linespacing=1.1, zorder=6)


def connect(axis: plt.Axes, start: tuple[float, float], end: tuple[float, float], color: str, *, dashed: bool = False) -> None:
    """Draw a trajectory segment with an understated directional arrow."""
    style = "--" if dashed else "-"
    axis.add_patch(
        FancyArrowPatch(
            start,
            end,
            arrowstyle="-|>",
            mutation_scale=10,
            linewidth=1.25,
            linestyle=style,
            color=color,
            shrinkA=6,
            shrinkB=7,
            zorder=4,
        )
    )


def draw_historical_panel(axis: plt.Axes) -> None:
    add_panel_frame(axis, "(a) Historical input sequence", BLUE)
    positions = ((0.16, 0.71), (0.37, 0.64), (0.58, 0.56), (0.79, 0.49))
    labels = (
        r"$C(t_0-3\,\mathrm{h})$",
        r"$C(t_0-2\,\mathrm{h})$",
        r"$C(t_0-1\,\mathrm{h})$",
        r"$C(t_0)$",
    )
    for start, end in zip(positions[:-1], positions[1:]):
        connect(axis, start, end, BLUE)
    axis.text(0.05, 0.823, "Historical storm track", fontsize=9.4, color=BLUE, fontstyle="italic")

    for index, ((x, y), label) in enumerate(zip(positions, labels)):
        add_storm_center(axis, x, y, BLUE, label)
        window_center = (x, 0.330)
        axis.plot((x, x), (y - 0.019, window_center[1] + 0.083), linestyle=(0, (3, 2)), color=BLUE, linewidth=0.78, zorder=1)
        add_patch_window(axis, window_center, 0.165, BLUE, "31 × 31\ninput patch")

    axis.text(
        0.50,
        0.125,
        "Each input patch is centered at the storm position available\nat the corresponding historical time.",
        ha="center",
        va="center",
        fontsize=8.9,
        color=DARK,
        linespacing=1.22,
    )
    axis.text(
        0.50,
        0.050,
        r"$X=\{W(t,C(t))\mid t\in\{t_0-3\,\mathrm{h},t_0-2\,\mathrm{h},t_0-1\,\mathrm{h},t_0\}\}$",
        ha="center",
        va="center",
        fontsize=8.7,
        color=DARK,
    )


def draw_correct_target_panel(axis: plt.Axes) -> None:
    add_panel_frame(axis, r"(b) Correct fixed-$t_0$ target", GREEN)
    initial = (0.29, 0.56)
    future = (0.74, 0.71)
    connect(axis, initial, future, GRAY)
    axis.text(0.51, 0.777, "Storm track after initialization", ha="center", fontsize=9.0, color=GRAY, fontstyle="italic")
    add_storm_center(axis, *initial, GREEN, r"$C(t_0)$")
    add_storm_center(axis, *future, ORANGE, r"$C(t_0+H)$")
    axis.text(0.74, 0.642, "future true storm center", ha="center", fontsize=8.2, color=ORANGE)

    axis.add_patch(
        Rectangle((0.10, 0.25), 0.79, 0.22, facecolor="#F2F5F3", edgecolor=LIGHT_GRAY, linewidth=0.65, zorder=1)
    )
    axis.text(0.50, 0.455, r"Future wind field at $t_0+H$", ha="center", va="bottom", fontsize=9.8, color=DARK)
    window_center = (initial[0], 0.355)
    axis.plot((initial[0], initial[0]), (initial[1] - 0.018, window_center[1] + 0.105), linestyle=(0, (3, 2)), color=GREEN, linewidth=0.95, zorder=2)
    add_patch_window(axis, window_center, 0.205, GREEN, "31 × 31 target\nextraction window")
    axis.text(0.50, 0.190, r"Target extraction window centered at $C(t_0)$", ha="center", va="top", fontsize=9.0, color=GREEN)
    axis.text(0.50, 0.114, r"$Y_H=W(t_0+H,C(t_0))$", ha="center", va="center", fontsize=13.0, color=DARK)
    axis.text(
        0.50,
        0.049,
        "Future wind values are used, but no future storm-position\ninformation is used.",
        ha="center",
        va="center",
        fontsize=8.8,
        color=DARK,
        linespacing=1.18,
    )


def draw_incorrect_panel(axis: plt.Axes) -> None:
    add_panel_frame(axis, "(c) Future-center target — not used", RED)
    initial = (0.25, 0.56)
    future = (0.69, 0.69)
    connect(axis, initial, future, GRAY, dashed=True)
    add_storm_center(axis, *initial, GRAY, r"$C(t_0)$", label_side="below")
    add_storm_center(axis, *future, ORANGE, r"$C(t_0+H)$")
    window_center = (future[0], 0.365)
    axis.plot((future[0], future[0]), (future[1] - 0.018, window_center[1] + 0.105), linestyle=(0, (3, 2)), color=RED, linewidth=0.9, zorder=2)
    add_patch_window(axis, window_center, 0.205, RED, "31 × 31 target\nwindow")
    axis.text(0.69, 0.196, r"Target centered at $C(t_0+H)$", ha="center", va="top", fontsize=8.9, color=RED)
    axis.text(0.50, 0.108, r"$W(t_0+H,C(t_0+H))$", ha="center", va="center", fontsize=12.0, color=RED)
    axis.text(
        0.50,
        0.047,
        "Requires future best-track position and\ncauses information leakage.",
        ha="center",
        va="center",
        fontsize=8.6,
        color=RED,
        linespacing=1.18,
    )
    axis.plot((0.08, 0.91), (0.18, 0.84), color=RED, linewidth=3.0, alpha=0.80, zorder=12)
    axis.plot((0.08, 0.91), (0.84, 0.18), color=RED, linewidth=3.0, alpha=0.80, zorder=12)
    axis.text(0.50, 0.857, "Not used", ha="center", va="bottom", fontsize=12.0, fontweight="bold", color=RED, zorder=13)


def main() -> None:
    script_path = Path(__file__).resolve()
    output_dir = script_path.parent.parent / "results" / "figures"
    output_dir.mkdir(parents=True, exist_ok=True)

    plt.rcParams.update(
        {
            "font.family": "serif",
            "font.serif": ["Times New Roman", "DejaVu Serif"],
            "mathtext.fontset": "dejavuserif",
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "svg.fonttype": "none",
        }
    )
    figure, axes = plt.subplots(
        1,
        3,
        figsize=(18.2, 6.7),
        facecolor="white",
        gridspec_kw={"width_ratios": (1.17, 1.12, 0.94), "wspace": 0.10},
    )
    draw_historical_panel(axes[0])
    draw_correct_target_panel(axes[1])
    draw_incorrect_panel(axes[2])

    output_paths = {
        "png": output_dir / "Figure_target_patch_construction.png",
        "svg": output_dir / "Figure_target_patch_construction.svg",
        "pdf": output_dir / "Figure_target_patch_construction.pdf",
    }
    figure.savefig(output_paths["png"], dpi=800, bbox_inches="tight", facecolor="white")
    figure.savefig(output_paths["svg"], bbox_inches="tight", facecolor="white")
    figure.savefig(output_paths["pdf"], bbox_inches="tight", facecolor="white")
    plt.close(figure)

    for output_path in output_paths.values():
        print(output_path.resolve())


if __name__ == "__main__":
    main()
