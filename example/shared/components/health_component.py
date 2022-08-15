from citrus import export
from citrus.core.component import component


@component()
class Health:
    health = 100

    def add_health(self, added_health):
        self.health += abs(added_health)

    def remove_health(self, removed_health):
        self.health = max(self.health - abs(removed_health), 0)

    def kill(self):
        self.health = 0


export(Health)
