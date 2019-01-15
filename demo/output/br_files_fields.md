
## Output files & attributes of the bike & ride analysis

**Files:**
- br_lines.shp        
    - lines between the first and last points of cycling legs
- br_origins.shp
    - first points of the cycling legs (center points of the HSY grid cells)
    - if two cycling legs depart from same origin, travel times are from the faster itinerary
- br_routes.shp
    - full geometries of the cycling legs
- br_hubs.shp
    - last points of the cycling legs
    - sum_pop: population of all related cycling legs (i.e. catchment of the hub)
    - avg_saving: sum of saved min / sum_pop (min)
- br_sum_hubs.shp
    - last points of the cycling legs, nearby points aggregated

**Fields:**
- hsy_idx:  HSY population grid cell id
- pop:  population
- tt_norm:  travel time by conventional public transport (walk & ride, min)
- tt_br:  travel time of bike & ride itinerary (min)
- tt_diff:  difference between tt_norm and tt_diff (min)
- tt_ratio:  relative difference (tt_diff/tt_norm, %)
- saved_min:  tt_diff * population (min)
- tt_b:  travel time of just the cycling leg (min)
- dist_b:  distance of the cycling leg (m)
