discogs_to_song_styles = {

    # -------------------------------------------------------------------------
    # BLUES
    # -------------------------------------------------------------------------
    # We place only the more obviously "acoustic" forms under "Acoustic"
    "Country Blues": "Acoustic",
    "Delta Blues": "Acoustic",
    "Piano Blues": "Acoustic",
    # "Rhythm & Blues" => mapped to "Beats" (R&B is groove-based)
    "Rhythm & Blues": "Beats",
    # The rest of the blues sub‐genres are omitted (no direct match)

    # -------------------------------------------------------------------------
    # BRASS & MILITARY
    # -------------------------------------------------------------------------
    # No direct "holiday," "kids," "acoustic," etc. - skipping

    # -------------------------------------------------------------------------
    # CHILDREN'S
    # -------------------------------------------------------------------------
    "Educational": "Kids",
    "Story": "Kids",

    # -------------------------------------------------------------------------
    # CLASSICAL
    # -------------------------------------------------------------------------
    # Group all classical sub-styles under "Traditional"
    "Baroque": "Traditional",
    "Choral": "Traditional",
    "Classical": "Traditional",
    "Contemporary": "Traditional",
    "Impressionist": "Traditional",
    "Medieval": "Traditional",
    "Modern": "Traditional",
    "Neo-Classical": "Traditional",
    "Neo-Romantic": "Traditional",
    "Opera": "Traditional",
    "Post-Modern": "Traditional",
    "Renaissance": "Traditional",
    "Romantic": "Traditional",

    # -------------------------------------------------------------------------
    # ELECTRONIC
    # -------------------------------------------------------------------------
    # If it’s very experimental/avant-garde => "Experimental"
    # If it’s heavily beat-driven => "Beats"
    # Otherwise, we skip
    "Abstract": "Experimental",
    "Acid": "Experimental",
    "Acid House": "Beats",
    "Acid Jazz": "Experimental", 
    "Ambient": "Experimental",
    "Breakbeat": "Beats",
    "Breakcore": "Experimental",
    "Chillwave": "Experimental",
    "Dark Ambient": "Experimental",
    "Drone": "Experimental",
    "Drum n Bass": "Beats",
    "Dub": "Beats",          # Jamaican-based groove
    "Dubstep": "Beats",
    "Illbient": "Experimental",
    "Musique Concrète": "Experimental",
    "Noise": "Experimental",
    "Trip Hop": "Beats",
    # The rest (e.g. “Hardstyle,” “Italo-Disco,” “Makina,” etc.) skipped

    # -------------------------------------------------------------------------
    # FOLK, WORLD, & COUNTRY
    # -------------------------------------------------------------------------
    # Typically "Traditional" if strongly folk-based, 
    # or "Kids" if specifically child-oriented
    "Bluegrass": "Traditional",
    "Cajun": "Traditional",
    "Celtic": "Traditional",
    "Folk": "Traditional",
    "Polka": "Traditional",
    # "Gospel" => skipped, no direct "Holiday"/"Kids"/"Ballad"/"Acoustic" fit

    # -------------------------------------------------------------------------
    # FUNK / SOUL
    # -------------------------------------------------------------------------
    # Funk/Soul typically groove-based => "Beats"
    "Afrobeat": "Beats",
    "Disco": "Beats",
    "Funk": "Beats",
    "Neo Soul": "Beats",
    "Soul": "Beats",
    "Rhythm & Blues": "Beats",  # repeated but that’s ok

    # -------------------------------------------------------------------------
    # HIP HOP
    # -------------------------------------------------------------------------
    # All forms of hip hop => "Beats"
    "Hip Hop": "Beats",
    "Boom Bap": "Beats",
    "Crunk": "Beats",
    "Grime": "Beats",
    "Pop Rap": "Beats",
    "Trap": "Beats",
    "Trip Hop": "Beats",  # repeated from above

    # -------------------------------------------------------------------------
    # JAZZ
    # -------------------------------------------------------------------------
    # "Free Jazz," "Avant-garde Jazz" => "Experimental"
    "Free Jazz": "Experimental",
    "Avant-garde Jazz": "Experimental",
    # "Dixieland," "Ragtime," etc. => "Traditional"
    "Dixieland": "Traditional",
    "Ragtime": "Traditional",
    "Swing": "Traditional",

    # -------------------------------------------------------------------------
    # LATIN
    # -------------------------------------------------------------------------
    # Latin folk/dance styles => "Traditional" if they're historically traditional
    "Cumbia": "Traditional",
    "Salsa": "Traditional",
    "Tango": "Traditional",
    "Samba": "Traditional",
    "Bossa Nova": "Acoustic",  # known for mellow acoustic guitar style

    # -------------------------------------------------------------------------
    # NON-MUSIC
    # -------------------------------------------------------------------------
    # "Audiobook", "Comedy", "Spoken Word", etc. => no direct match => skip

    # -------------------------------------------------------------------------
    # POP
    # -------------------------------------------------------------------------
    # "Ballad" => "Ballad"
    "Ballad": "Ballad",
    # Others like "Bubblegum," "Europop," etc. => skip

    # -------------------------------------------------------------------------
    # REGGAE
    # -------------------------------------------------------------------------
    # Typically groove-based => "Beats"
    "Dancehall": "Beats",
    "Rocksteady": "Beats",
    "Ska": "Beats",
    "Reggae": "Beats",

    # -------------------------------------------------------------------------
    # ROCK
    # -------------------------------------------------------------------------
    # "Acoustic" if it explicitly says "Acoustic"
    "Acoustic": "Acoustic",
    # Some experimental forms of rock => "Experimental"
    "Acid Rock": "Experimental",
    "Folk Rock": "Traditional",  # merges folk & rock
    "Psychedelic Rock": "Experimental",
    # "Christmas" or "Holiday" => if "Christmas Rock" existed, we’d do so
    # Everything else => no direct style => skip

    # -------------------------------------------------------------------------
    # STAGE & SCREEN
    # -------------------------------------------------------------------------
    # "Christmas Music" => "Holiday" or "Christmas"
    # If “Christmas Music” were explicitly present, we’d do "Christmas"
    # Otherwise we skip "Musical", "Score", "Soundtrack", "Theme"
}
