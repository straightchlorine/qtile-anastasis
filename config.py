from typing import List  # noqa: F401

import os
import subprocess
from libqtile import bar, layout, widget, hook
from libqtile.config import Click, Drag, Group, Key, KeyChord, Match, Screen, ScratchPad, DropDown
from libqtile.lazy import lazy
from time import time
from pathlib import Path

mod = "mod4"                            # windows key as super key
terminal = "alacritty -e fish"          # default terminal

keys = [                                # binds
    # elementary qtile functions
        Key([mod, "control"], "r",
            lazy.restart(), desc="restart"),
        Key([mod, "control"], "q",
            lazy.shutdown(), desc="shutdown"),
        Key([mod], "Return",
            lazy.spawn(terminal), desc="terminal"),
        Key([mod, "shift"], "Return",
            lazy.spawn("/home/goldberg/.config/rofi/bin/launcher_text"), desc="launcher"),
        Key([mod], "Tab",
            lazy.next_layout(), desc="toggle between layouts"),
        Key([mod, "shift"], "c",
            lazy.window.kill(), desc="kill active window"),

    # focus management 
        # switching focus between windows
            Key([mod], "h",
                lazy.layout.left(), desc="focus to the left"),
            Key([mod], "l",
                lazy.layout.right(), desc="focus to the right"),
            Key([mod], "j",
                lazy.layout.down(), desc="focus down"),
            Key([mod], "k",
                lazy.layout.up(), desc="focus up"),
            Key([mod], "space",
                lazy.layout.next(), desc="focus to the other window"),

        # switching focus between motnitors
            Key([mod], "period",
                lazy.next_screen(), desc='Move focus to next monitor'),
            Key([mod], "comma",
                lazy.prev_screen(), desc='Move focus to prev monitor'),

        # moving windows
            Key([mod, "shift"], "h",
                lazy.layout.shuffle_left(), desc="window to the left"),
            Key([mod, "shift"], "l",
                lazy.layout.shuffle_right(), desc="window to the right"),
            Key([mod, "shift"], "j",
                lazy.layout.shuffle_down(), desc="window down"),
            Key([mod, "shift"], "k",
                lazy.layout.shuffle_up(), desc="window up"),

        # window size management
            # by direction
                Key([mod, "control"], "h",
                    lazy.layout.grow_left(), desc="expand window to the left"),
                Key([mod, "control"], "l",
                    lazy.layout.grow_right(), desc="expand window to the right"),
                Key([mod, "control"], "j",
                    lazy.layout.grow_down(), desc="expand window down"),
                Key([mod, "control"], "k",
                    lazy.layout.grow_up(), desc="expand window up"),

            # regular
                Key([mod], "i",
                    lazy.layout.grow()),
                Key([mod], "m",
                    lazy.layout.shrink()),

            # general functions
                Key([mod], "o",
                    lazy.layout.maximize()),
                Key([mod], "n",
                    lazy.layout.normalize()),
                Key([mod], "f",
                    lazy.window.toggle_fullscreen())
]

colors = []                                 # list of colors
cache = "/home/goldberg/.cache/wal/colors"  # directory, where wpgtk dumps generated colors, based on the image

# function loading the colors from cache directory
def load_colors(cache):
    with open(cache, "r") as file:
        for _ in range(15):
            colors.append(file.readline().strip())
    lazy.reload()

# loading the colors
load_colors(cache)

# timezone setter
def set_timezone(timezone):
    os.environ['TZ'] = timezone
    time.tzset()

# set_timezone('Europe/London')

# group names and preferred layout
group_names = [("Internet",         {'layout': 'monadtall'}),
               ("Dev",              {'layout': 'monadtall'}),
               ("Side Dev",         {'layout': 'monadtall'}),
               ("System",           {'layout': 'monadtall'}),
               ("Documentation",    {'layout': 'monadtall'}),
               ("Music",            {'layout': 'monadtall'}),
               ("Video",            {'layout': 'monadtall'}),
               ("Files",            {'layout': 'monadtall'}),
               ("Nothing",          {'layout': 'zoomy'})]

# populating groups, based on the group_names
groups = [
    Group(name, **kwargs) for name, kwargs in group_names
]

# assigning a number for every single tuple in group_names
# responsible for switching groups and sending windows from 
# one to another
for i, (name, kwargs) in enumerate(group_names, 1):
    keys.append(Key([mod], str(i), lazy.group[name].toscreen()))        # switch to another group
    keys.append(Key([mod, "shift"], str(i), lazy.window.togroup(name))) # send a window to another gruop


# defining a drop-down terminal
groups.append(
    ScratchPad("scratchpad", [
        DropDown("term", terminal, opacity=0.9)
    ])
)
keys.extend([
    Key([mod], 'd',
        lazy.group['scratchpad'].dropdown_toggle('term')),
])

layout_theme = {
    "border_width"  : 1,
    "margin"        : 16,
    "border_normal" : colors[0],
    "border_focus"  : colors[6],
}

layouts = [
    # layout.Columns(border_focus_stack='#d75f5f', **layout_theme),
    # layout.Max(**layout_theme),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    layout.MonadTall(**layout_theme),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    layout.Zoomy(**layout_theme),
]

widget_defaults = dict(
    font        = "SourceCodePro",
    fontsize    = 13,
    padding     = 3,
    foreground=colors[7],
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.GroupBox(
                    disable_drag                = True,
                    block_highlight_text_color  = colors[10],
                    active                      = colors[7],
                    this_current_screen_border  = colors[13],
                    this_screen_border          = colors[14],
                    other_screen_border         = colors[12],
                    highlight_method            = 'text',
                    highlight_color             = [colors[14], colors[12]],
                    urgent_alert_method         = 'text',
                    urgent_border               = colors[9],
                    urgent_text                 = colors[9],
                    hide_unused                 = True,
                ),
                widget.Sep(
                    linewidth                   = 0,
                    size_percent                = 40,
                    padding                     = 25,
                ),
                widget.WindowName(
                    format                      = '',
                ),
                widget.CPU(
                    fontsize                    = 10,
                    format                      = ' CPU {load_percent}% ',
                ),
                widget.Sep(
                    size_percent                = 30,
                ),
                widget.Memory(
                    fontsize                    = 10,
                    format                      = ' RAM {MemPercent}% ',
                ),
                widget.Sep(
                    size_percent                = 40,
                ),
                widget.Net(
                    fontsize                    = 10,
                    interface                   = 'enp3s0',
                    format                      = ' {down} ↓↑ {up} ',
                ),
                widget.Sep(
                    linewidth                   = 0,
                    size_percent                = 40,
                    padding                     = 485,
                ),
                widget.Clock(
                    format                      = '%A, %d %B %Y, %H:%M:%S',
                    padding                     = 25,
                ),
            ],
            30,
            margin=[16, 16, 0, 16],  # N E S W
            background=colors[0],
        ),
    ),
    Screen(),
]


# floating windows
mouse = [
    Drag([mod], "Button1",
        lazy.window.set_position_floating(), start=lazy.window.get_position(),),
    Drag([mod], "Button3",
         lazy.window.set_size_floating(), start=lazy.window.get_size(),),
    Click([mod], "Button2",
          lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
main = None  # WARNING: this is deprecated and will be removed soon
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ],
    **layout_theme
)
auto_fullscreen = False
focus_on_window_activation = "smart"

# startup

@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('~/.config/qtile/scripts/autostart.sh')
    subprocess.call([home])

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
