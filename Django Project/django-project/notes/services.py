from notes.models import Note, NoteReaction


def set_note_reaction(note: Note, user, reaction: str) -> None:
    status = NoteReaction.objects.filter(note=note, user=user).update(reaction=reaction)
    # Если уже была реакция.
    if status:
        return

    NoteReaction.objects.create(note=note, user=user, reaction=reaction)
