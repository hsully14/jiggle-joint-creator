# Control curve creation utilities - shapes dictionary and helper functions

import maya.cmds as mc
import pymel.core as pm
import maya.api.OpenMaya as om


# ************************************************************************************
# HELPER FUNCTIONS
# ************************************************************************************
def rename_skincluster(objects=[]):
    """Renames skinclusters based on object name. Helper function for copy_skin_cluster.

    Arguments:
        objects (list): objects with skinclusters

    Returns:
        new_skin_cluster (list): renamed skinclusters
    """
    # TODO: verify this refactor works as expected

    if not objects:
        objects = mc.ls(sl=True)

    for object in objects:
        inputs = mc.listHistory(object, interestLevel=1)
        skin_cluster = mc.ls(inputs, type='skinCluster')
        if skin_cluster:
            new_skin_cluster = mc.rename(skin_cluster[0], 'skinCluster_{}'.format(object))
    
    #TODO: eval this return
    return new_skin_cluster


def copy_skin_cluster(skinned_mesh, target_meshes=[], rename=True):
    """Copies skin cluster with identical influences from first selected object to all 
    other selections.

    Args:
        skinned_mesh (string): mesh to copy skinning from
        target_meshes (list): list of meshes to copy skinning to
        rename (bool): whether to rename the new skinclusters or take name from geo

    Returns:
        new_skin_cluster_names (list): newly created skinclusters
    """
    # TODO: verify this refactor works as expected
    maxInfluences = 0
    maintainMaxInfluences = False
    new_skin_cluster_names = []

    skin_cluster = mc.ls(mc.listHistory(skinned_mesh), type='skinCluster')

    if skin_cluster:
        maintainMaxInfluences = mc.getAttr('{}.maintainMaxInfluences'.format(skin_cluster[0]))
        maxInfluences = mc.getAttr('{}.maxInfluences'.format(skin_cluster[0]))

    for mesh in target_meshes:
        # remove existing skincluster
        old_skin_cluster = mc.ls(mc.listHistory(skinned_mesh), type='skinCluster')
        if old_skin_cluster:
            mc.delete(old_skin_cluster)

        joints = mc.skinCluster(skin_cluster[0], weightedInfluence=True, query=True)

        new_skin_cluster = mc.skinCluster(joints, mesh, toSelectedBones=True)[0]

        mc.setAttr('{}.maintainMaxInfluences'.format(new_skin_cluster), maintainMaxInfluences)
        mc.setAttr('{}.maxInfluences'.format(new_skin_cluster), maxInfluences)

        mc.copySkinWeights(sourceSkin=skin_cluster[0],
                           destinationSkin=new_skin_cluster,
                           notMirror=True,
                           surfaceAssociation='closestPoint')

        if rename:
            new_skin_cluster_name = rename_skincluster(objects=[mesh])
        else:
            new_skin_cluster_name = new_skin_cluster
        new_skin_cluster_names.append(new_skin_cluster_name)

    return new_skin_cluster_names


def add_joints_to_skincluster(skinned_mesh, joints=[]):
    """Add given joints into given mesh skincluster with locked, zeroed weights

    Arguments:
        joints (list): names of joints to add
        skinned_mesh (string): target skinned geo
    """
    #get skin cluster from skinned mesh
    skin_cluster = mc.ls(mc.listHistory(skinned_mesh), type='skinCluster')

    for joint in joints:
        mc.skinCluster(skin_cluster, edit=True, lockWeights=True, weight=0, addInfluence=joint)


def duplicate_selected_faces():
    """Creates a copy geometry of selected faces.

    Returns:
        selected_object (string): selected original mesh
        duped_object (string): duplicated face geometry
    """

    # TODO: refactor this to work with button press? and be smarter, store/share data?
    selected_faces = mc.ls(sl=True)

    selected_object = selected_faces[0].split('.')[0]
    duped_object = mc.duplicate(selected_object)[0]

    keepable_geo = []

    for face in selected_faces:
        face = face.replace(selected_object, duped_object)
        keepable_geo.append(face)

    clear_selection()

    # select faces on duplicate geometry, invert selection, and delete remaining faces
    mc.select(keepable_geo)
    mc.select(duped_object + '.f[*]', toggle=True)
    delete_faces = mc.ls(sl=True)
    mc.delete(delete_faces)

    # freeze transforms and clear history on duplicate
    mc.makeIdentity(duped_object, apply=True)
    mc.delete(duped_object, constructionHistory=True)

    # hide original object for visual clarity
    mc.hide(selected_object)

    return selected_object, duped_object


def get_selected_verts():
    """Returns selected verts in an ordered selection list"""
    verts = mc.ls(orderedSelection=True)
    return verts


def clear_selection():
    mc.select(clear=True)


def create_locs_on_verts(base_geometry):
    """Creates locators on selected verts on given base geometry object

    Returns:
        locs (list): list of duplicated locators
        vert_loc_pairs (dict): dict of locs and matching vert pairs
    """
    # FIXME: save vertex selection data as part of class variable, something more accessible?
    verts = get_selected_verts()
    locs = []
    vert_loc_pairs = {}

    for index, vert in enumerate(verts):
        # format index to 2 digit number and add 1 for prettier iteration counting
        naming_index = '{0:0=2d}'.format(index+1)

        #create locator, get vertex position, and match loc to vert
        loc = mc.spaceLocator(name='loc_{0}_{1}'.format(base_geometry, naming_index))
        vert_location = mc.xform(vert, query=True, worldSpace=True, translation=True)
        mc.xform(loc, worldSpace=True, translation=vert_location)

        # collect data
        locs.append(loc)
        vert_loc_pairs[vert] = loc

    for loc in locs:
        # align locator to nearest normal
        constraint = mc.normalConstraint(base_geometry, loc, aimVector=(1, 0, 0), worldUpType=0)
        mc.delete(constraint)

    return locs, vert_loc_pairs


def get_vertex_uvs(vert):
    '''Returns list of vertex UV coordinates. Only works on 1 vert.'''
    # FIXME: need unified reference variable for selected verts

    mc.select(vert)
    mc.ConvertSelectionToUVs()
    uv_values = mc.polyEditUV(query=True)

    return uv_values


def create_uv_pin(name, side, base_geometry):
    pin_name = 'F_{}_{}_UVPin'.format(side, name)

    # create uvPin node, set temp axes
    uv_pin = mc.createNode('uvPin', name=pin_name)
    mc.setAttr('{}.normalAxis'.format(uv_pin), 0)
    mc.setAttr('{}.tangentAxis'.format(uv_pin), 5)

    base_geometry_shape = mc.listRelatives(base_geometry)[0]
    shape_orig = mc.deformableShape(base_geometry_shape, createOriginalGeometry=True)

    # connect pin to base_geometry 
    mc.connectAttr(shape_orig[0], '{}.originalGeometry'.format(uv_pin))
    mc.connectAttr('{}.worldMesh[0]'.format(base_geometry_shape), '{}.deformedGeometry'.format(uv_pin))

    return uv_pin



# ************************************************************************************
# FIXME: working to refactor this, keeping original here for safekeeping
# ************************************************************************************
# def copySkinCluster(source='', dest=[], rename=False):
#     maxInfluences = 0
#     maintainMaxInfluences = False
#     if not source and not dest:
#         objects = mc.ls(sl=True)
#         if len(objects) < 2:
#             return False
#         else:
#             source = objects[0]
#             dest = objects[1:]
#     sourceHistory = mc.listHistory(source, lv=1)
#     sc = mc.ls(sourceHistory, typ='skinCluster')
#     if sc:
#         maintainMaxInfluences = mc.getAttr('{}.maintainMaxInfluences'.format(
#             sc[0]))
#         maxInfluences = mc.getAttr('{}.maxInfluences'.format(sc[0]))
#     newSCNames = []
#     for d in dest:
#         destHistory = mc.listHistory(d, lv=1)
#         oldSC = mc.ls(destHistory, typ='skinCluster')
#         if oldSC:
#             mc.delete(oldSC)
#         jnts = mc.skinCluster(sc[0], weightedInfluence=True, q=True)
#         newSC = mc.skinCluster(jnts, d, tsb=True)[0]
#         mc.setAttr('{}.maintainMaxInfluences'.format(newSC),
#                    maintainMaxInfluences)
#         mc.setAttr('{}.maxInfluences'.format(newSC), maxInfluences)
#         mc.copySkinWeights(ss=sc[0],
#                            ds=newSC,
#                            nm=True,
#                            surfaceAssociation='closestPoint')
#         if rename:
#             pass
#             newSCName = renameDeformers(objects=[d])
#         else:
#             newSCName = newSC
#         newSCNames.append(newSCName)
#     #mc.select(objects)
#     return (newSCNames) 

