# Map-Maker-2

A top-down FPS map designer for phones, used to block out levels before rebuilding them in Unreal.

The whole app is one file: `map-designer.html`. It's published as a private Claude artifact and runs in the phone's browser.

## What it does (v6)

- Main menu: New Blank, Maps, Shapes & Symbols, Bestiary, Settings, and Continue. Each opens a full page.
- Shapes & Symbols: a Shape Builder for custom shapes made from circles and polygons. Every placed copy is an instance of the saved master, so editing the master updates them all; Break apart turns one copy back into plain shapes.
- Symbols (ammo, health, objective, exit…) with a name, icon, color and letter; make your own.
- Multi-select (tap or box-select), Group/Ungroup, and Save selection as a custom shape.
- Doors: snap onto room walls and cut a gap; each door either locks until its room is cleared or stays open.
- Bestiary: enemy types shared by every map, with an attack type (melee, hitscan, projectile), movement style (rush, hold, keep distance), health, speed, damage, attack rate, range, accuracy and notes.
- Simulate: the current floor becomes a walking grid; the player explores and fights, enemies wake on sight or sound, and entering a room with enemies locks its doors until it is clear. Play, pause, 1×/2×/4×, restart.
- The simulated player plays Doom-style by default (keeps moving, strafes, pushes in close); a Settings slider runs to Tactical, and its health, speed, damage, fire rate, accuracy and range are editable. An Objective or Exit symbol becomes the player's goal.
- Run 10×: ten seeded runs in about a second, with a results list, exact replays of any run, all trails overlaid, a damage heatmap, per-room clear stats and damage by enemy type.
- Grid where 1 square = 1 m (100 Unreal units). Pinch to zoom, drag empty space to pan.
- Shapes are Rooms (floor + walls) or Solids (crates, pillars). Overlapping rooms join: the walls between them dissolve, or a setting keeps a dividing wall.
- Circles, and polygons with a sides slider (3–12: triangle, square, pentagon … dodecagon).
- Drag to move, corner handles to resize, top handle to rotate. A slim bar shows when something is selected; More has exact size, position and rotation.
- Player markers (blue, with a facing direction) and colored enemy markers: drag up from the tray, or tap one and then tap the map. Types can be renamed and recolored.
- Multiple floors with a switcher. The floor below shows faintly.
- Snap (0.25/0.5/1 m, 5/15/45°), undo/redo.
- Lock the whole map, lock single objects, or lock just an object's size.
- Settings for room wall thickness, room floor opacity, solid outline thickness and solid fill opacity.
- Shape merging uses polygon-clipping 0.15.7 from jsDelivr.
- Autosave to the Claude account (falls back to the browser), plus backup files (.json) and a PNG of a floor.
