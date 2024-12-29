class GemeindewappenDBRouter:
    """
    Ein Datenbankrouter, der alle Operationen für das Wappen-Modell auf die 'gemeindewappen' Datenbank umleitet.
    Gleichzeitig verhindern wir Migrationen auf dieser Datenbank.
    """
    def db_for_read(self, model, **hints):
        """Gibt die Datenbank zurück, die für das Lesen eines Modells verwendet werden soll."""
        if model._meta.app_label == 'gemeindewappen_website':
            return 'gemeindewappen'  # Datenbank für Wappen-Daten
        return None

    def db_for_write(self, model, **hints):
        """Gibt die Datenbank zurück, die für das Schreiben eines Modells verwendet werden soll."""
        if model._meta.app_label == 'gemeindewappen_website':
            return 'gemeindewappen'  # Datenbank für Wappen-Daten
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """Gibt an, ob eine Beziehung zwischen zwei Objekten in unterschiedlichen Datenbanken erlaubt ist."""
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """Bestimmt, ob Migrationen für ein bestimmtes Modell und eine bestimmte Datenbank zugelassen sind."""
        if db == 'gemeindewappen':
            return False 
