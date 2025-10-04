from .story_weaver import StoryWeaver
from .story_transformer import StoryTransformer
from .code_forger import CodeForger
from .comic_crafter import ComicCrafter
from .voice_forge import VoiceForge

HEAD_REGISTRY = {
    "story_weaver": StoryWeaver,
    "story_transformer": StoryTransformer,
    "code_forger": CodeForger,
    "comic_crafter": ComicCrafter,
    # "voice_forge": VoiceForge,
}
