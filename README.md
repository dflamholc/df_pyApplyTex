# df_pyApplyTex
apply textures to objects in C4D based on object naming

this script applies materials to objects based on name matching

at the current version _v13 name matching is absolute, but is planned to become token based - parsing each name to find a pattern

materials are applied to objects using cubic or uvw mapping, depending on whether the object already has a uvw tag

if an object already has tex/material tag with a matching name, no further material tag will be added -
thus runnign the script several times without changing the objects in the scene will not add further materials
