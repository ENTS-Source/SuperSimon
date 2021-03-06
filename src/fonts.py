import pygame

fontEntsCondensedItalicPath = "fonts/LeagueGothic-CondensedItalic.otf"
fontEntsCondensedRegularPath = "fonts/LeagueGothic-CondensedRegular.otf"
fontEntsItalicPath = "fonts/LeagueGothic-Italic.otf"
fontEntsRegularPath = "fonts/LeagueGothic-Regular.otf"

# Generic
SMALL_FONT = pygame.font.Font(fontEntsRegularPath, 12)
THIN_FONT = pygame.font.Font(fontEntsRegularPath, 25)
REGULAR_FONT = pygame.font.Font(fontEntsRegularPath, 45)
MEDIUM_FONT = pygame.font.Font(fontEntsRegularPath, 55)
LARGE_FONT = pygame.font.Font(fontEntsRegularPath, 65)
EXTRA_LARGE_FONT = pygame.font.Font(fontEntsRegularPath, 90)
SUPER_LARGE_FONT = pygame.font.Font(fontEntsRegularPath, 110)
SUPER_EXTRA_LARGE_FONT = pygame.font.Font(fontEntsRegularPath, 160) # dat name

# Specific
HEADER_FONT = SUPER_EXTRA_LARGE_FONT
SUBTITLE_FONT = MEDIUM_FONT
LEADERBOARD_RANK_FONT = REGULAR_FONT
LEADERBOARD_SCORE_FONT = LARGE_FONT
PLAYER_SUBTEXT1_FONT = REGULAR_FONT
PLAYER_SUBTEXT2_FONT = THIN_FONT
PLAYER_NUMBER_FONT = REGULAR_FONT
PLAYER_MAJOR_FONT = LARGE_FONT
TOTALS_FONT = REGULAR_FONT
