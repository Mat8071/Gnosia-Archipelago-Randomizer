from dataclasses import dataclass

@dataclass()
class CharacterStats:

    charisma: float = 0.0
    intuition: float = 0.0
    charm: float = 0.0
    logic: float = 0.0
    performance: float = 0.0
    stealth: float = 0.0


npc_starting_stats: dict[str, CharacterStats] = {
    "Gina": CharacterStats(3.5, 4, 7.5, 10, 2, 9),
    "SQ": CharacterStats(5.5, 11, 15.5, 2.5, 14.5, 3),
    "Raqio": CharacterStats(3, 0.5, 2, 20.5, 11, 4.5),
    "Stella": CharacterStats(7.5, 5, 1.5, 13, 5, 7.5),
    "Shigemichi": CharacterStats(17, 3.5, 0.5, 2, 0.5, 16),
    "Chipie": CharacterStats(10, 17, 13.5, 7.5, 10.5, 15),
    "Remnan": CharacterStats(2, 21, 10, 15, 13, 22.5),
    "Comet": CharacterStats(5.5, 25.5, 11, 0.5, 4.5, 7.5),
    "Yuriko": CharacterStats(25.5, 20.5, 17.5, 22, 25, 12),
    "Jonas": CharacterStats(16.5, 9.5, 7, 12, 19.5, 15.5),
    "Setsu": CharacterStats(10, 8, 11, 12, 9.5, 3.5),
    "Otome": CharacterStats(7.5, 16.5, 20.5, 24, 11, 13.5),
    "Sha-Ming": CharacterStats(14.5, 5.5, 16.5, 6.5, 20.5, 25),
    "Kukrushka": CharacterStats(4.5, 16, 22.5, 0.5, 20.5, 17.5),
}

npc_final_stats: dict[str, CharacterStats] = {
    "Gina": CharacterStats(17.5, 45.5, 24, 31.5, 13, 31.5),
    "SQ": CharacterStats(22, 21.5, 46, 12, 47.5, 38.5),
    "Raqio": CharacterStats(16.5, 0.5, 7.5, 49.5, 35.5, 20.5),
    "Stella": CharacterStats(27, 18, 27.5, 42, 30.5, 29),
    "Shigemichi": CharacterStats(45.5, 14.5, 17.5, 9.5, 6, 45),
    "Chipie": CharacterStats(25, 39, 31, 18.5, 26.5, 33.5),
    "Remnan": CharacterStats(2, 41, 29, 28, 33, 43.5),
    "Comet": CharacterStats(17, 49.5, 32.5, 0.5, 16.5, 22),
    "Yuriko": CharacterStats(49.5, 42, 37.5, 44, 49.5, 25),
    "Jonas": CharacterStats(38.5, 25, 21.5, 34, 43.5, 37),
    "Setsu": CharacterStats(35, 28.5, 36.5, 38.5, 31, 17.5),
    "Otome": CharacterStats(16, 32, 42, 46.5, 23, 26.5),
    "Sha-Ming": CharacterStats(29, 6.5, 34.5, 6.5, 40.5, 49.5),
    "Kukrushka": CharacterStats(14, 35.5, 49.5, 3.5, 45, 40.5),
}

skill_stat_requirements: dict[str, CharacterStats] = {
        "Step Forward": CharacterStats(9.5, 0, 0, 0, 0, 0),
        "Definite Human/Enemy": CharacterStats(0, 0, 0, 19.5, 0, 0),
        "Definite AC Follower": CharacterStats(0, 0, 0, 24.5, 0, 0),
        "Definite Bug": CharacterStats(0, 0, 0, 29.5, 0, 0),
        "Say You're Human": CharacterStats(0, 19.5, 0, 0, 0, 0),
        "Vote": CharacterStats(0, 0, 0, 9.5, 0, 0),
        "Don't Vote": CharacterStats(0, 0, 0, 14.5, 0, 0),
        "Small Talk": CharacterStats(0, 0, 0, 0, 0, 9.5),
        "Freeze All": CharacterStats(0, 0, 0, 29.5, 0, 0),
        "Let's Collaborate": CharacterStats(0, 0, 14.5, 0, 0, 0),
        "Seek Agreement": CharacterStats(24.5, 0, 0, 0, 0, 0),
        "Block Argument": CharacterStats(39.5, 0, 0, 0, 0, 0),
        "Exaggerate": CharacterStats(0, 0, 0, 0, 14.5, 0),
        "Obfuscate": CharacterStats(0, 0, 0, 0, 0, 24.5),
        "Retaliate": CharacterStats(0, 0, 0, 24.5, 24.5, 0),
        "Regret": CharacterStats(0, 0, 24.5, 0, 0, 0),
        "Seek Help": CharacterStats(0, 0, 0, 0, 29.5, 0),
        "Don't Be Fooled": CharacterStats(0, 29.5, 0, 0, 0, 0),
        "Grovel": CharacterStats(0, 0, 0, 0, 0, 34.5),
}