# Map-Maker-2

A top-down FPS map designer for phones, used to block out levels before rebuilding them in Unreal.

The whole app is one file: `map-designer.html`. It's published as a private Claude artifact and runs in the phone's browser.

## What it does (v4)

- Main menu: New Blank, Maps, Shapes & Symbols, Bestiary, Settings, and Continue. Each opens a full page.
- Shapes & Symbols: a Shape Builder for custom shapes made from circles and polygons. Every placed copy is an instance of the saved master, so editing the master updates them all; Break apart turns one copy back into plain shapes.
- Symbols (ammo, health, objective, exit…) with a name, icon, color and letter; make your own.
- Multi-select (tap or box-select), Group/Ungroup, and Save selection as a custom shape.
- Bestiary: enemy types shared by every map, with health, speed, range, accuracy and notes.
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
