import contextlib
import jishaku.paginators
import jishaku.exception_handling
import discord
import re
from typing import Union
from collections import namedtuple

EmojiSettings = namedtuple('EmojiSettings', 'start back forward end close')

class FakeEmote(discord.PartialEmoji):
    """
    Due to the nature of jishaku checking if an emoji object is the reaction, passing raw str into it will not work.
    Creating a PartialEmoji object is needed instead.
    """
    @classmethod
    def from_name(cls, name):
        emoji_name = re.sub("|<|>", "", name)
        a, name, id = emoji_name.split(":")
        return cls(name=name, id=int(id), animated=bool(a))

emote = EmojiSettings(
    start=FakeEmote.from_name("<a:loading:782995523404562432>"),
    back=FakeEmote.from_name("<:before_check:754948796487565332>"),
    forward=FakeEmote.from_name("<:next_check:754948796361736213>"),
    end=FakeEmote.from_name("<:blobstop:749111017778184302>"),
    close=FakeEmote.from_name("<:redTick:596576672149667840>")
)
jishaku.paginators.EMOJI_DEFAULT = emote  # Overrides jishaku emojis

async def attempt_add_reaction(msg: discord.Message, reaction: Union[str, discord.Emoji]):
    """
    This is responsible for every add reaction happening in jishaku. Instead of replacing each emoji that it uses in
    the source code, it will try to find the corresponding emoji that is being used instead.
    """
    reacts = {
        "\N{WHITE HEAVY CHECK MARK}": "<:checkmark:753619798021373974>",
        "\N{BLACK RIGHT-POINTING TRIANGLE}": emote.forward,
        "\N{HEAVY EXCLAMATION MARK SYMBOL}": "<:information_pp:754948796454010900>",
        "\N{DOUBLE EXCLAMATION MARK}": "<:crossmark:753620331851284480>",
        "\N{ALARM CLOCK}": emote.end
    }
    react = reacts[reaction] if reaction in reacts else reaction
    with contextlib.suppress(discord.HTTPException):
        return await msg.add_reaction(react)

jishaku.exception_handling.attempt_add_reaction = attempt_add_reaction

def setup(bot):
    pass