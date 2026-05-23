from whitenoise.storage import CompressedManifestStaticFilesStorage


class ProfimizeStaticStorage(CompressedManifestStaticFilesStorage):
    # CKEditor ships bootstrap with sourcemap references that are not included.
    # Overriding hashed_name to silently skip missing referenced files rather
    # than raising MissingFileError during collectstatic.

    def hashed_name(self, name, content=None, filename=None):
        try:
            return super().hashed_name(name, content, filename)
        except Exception:
            return name
