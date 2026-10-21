# Map-Maker-2

A top-down FPS map designer for phones, used to block out levels before rebuilding them in Unreal.

The whole app is one file: `map-designer.html`. It's published as a private Claude artifact and runs in the phone's browser.

## What it does (v1)

- Grid where 1 square = 1 m (100 Unreal units). Pinch to zoom, drag empty space to pan.
- Circles, and polygons with a sides slider (3–12: triangle, square, pentagon … dodecagon).
- Drag to move, corner handles to resize, top handle to rotate. Exact size, position and rotation in the properties panel.
- Colored enemy markers: drag up from the tray, or tap one and then tap the map. Types can be renamed and recolored.
- Multiple floors with a switcher. The floor below shows faintly.
- Snap to 0.5 m and 15°, undo/redo.
- Autosave to the Claude account (falls back to the browser), plus backup files (.json) and a PNG of a floor.
