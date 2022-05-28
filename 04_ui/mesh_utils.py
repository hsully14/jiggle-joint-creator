# Control curve creation utilities - shapes dictionary and helper functions
import maya.cmds as mc
import control_curve_utils as ccu


# ************************************************************************************
# HELPER FUNCTIONS
# ************************************************************************************
def rename_skincluster(object=[]):
    """Renames skinclusters based on object name. Helper function for copy_skin_cluster.

    Arguments:
        objects (list): objects with skinclusters

    Returns:
        new_skin_cluster (list): renamed skinclusters
    """
    # TODO: verify this refactor works as expected


    inputs = mc.listHistory(object, interestLevel=1)
    skin_cluster = mc.ls(inputs, type='skinCluster')
    if skin_cluster:
        new_skin_cluster = mc.rename(skin_cluster[0], 'skinCluster_{}'.format(object))
    
    #TODO: eval this return
    return new_skin_cluster


def copy_skincluster(skinned_mesh='', target_mesh='', rename=True):
    max_influences = 0
    maintain_max_influences = False

    skin = find_skincluster(skinned_mesh)
    if not skin:
        mc.error('No skinCluster found in source history.')
        return

    maintain_max_influences = mc.getAttr(
        '{}.maintainMaxInfluences'.format(skin))
    max_influences = mc.getAttr('{}.maxInfluences'.format(skin))
    new_skin_names = []
    
    old_skin = find_skincluster(target_mesh)
    if old_skin:
        mc.delete(old_skin)
    joints = mc.skinCluster(skin, weightedInfluence=True, q=True)
    new_skin = mc.skinCluster(joints, target_mesh, tsb=True)[0]
    mc.setAttr('{}.maintainMaxInfluences'.format(new_skin),
                    maintain_max_influences)
    mc.setAttr('{}.maxInfluences'.format(new_skin), max_influences)
    mc.copySkinWeights(ss=skin,
                            ds=new_skin,
                            nm=True,
                            surfaceAssociation='closestPoint')
    if rename:
        new_skin_name = rename_skincluster(object=target_mesh)
    else:
        new_skin_name = new_skin
    new_skin_names.append(new_skin_name)
    # mc.select(objects)
    return new_skin_names


def find_skincluster(skin_object):
    skin_shape = None
    skin_shape_with_path = None
    hidden_shape = None
    hidden_shape_with_path = None

    control_point_test = mc.ls(skin_object, typ="controlPoint")
    if len(control_point_test):
        skin_shape = skin_object

    else:
        relatives = mc.listRelatives(skin_object)
        if relatives is None:
            return False
        for relative in relatives:
            control_point_test = mc.ls("{}|{}".format(skin_object, relative),
                             typ="controlPoint")
            if len(control_point_test) == 0:
                continue

            io = mc.getAttr("{}|{}.io".format(skin_object, relative))
            if io:
                continue

            visible = mc.getAttr("{}|{}.v".format(skin_object, relative))
            if not visible:
                hidden_shape = relative
                hidden_shape_with_path = "{}|{}".format(skin_object, relative)
                continue

            skin_shape = relative
            skin_shape_with_path = "{}|{}".format(skin_object, relative)
            break

    if skin_shape:
        if len(skin_shape) == 0:
            if len(hidden_shape) == 0:
                return None

            else:
                skin_shape = hidden_shape
                skin_shape_with_path = hidden_shape_with_path

    clusters = mc.ls(typ="skinCluster")
    for cluster in clusters:
        geometry = mc.skinCluster(cluster, q=True, g=True)
        for geo in geometry:
            if geo == skin_shape or geo == skin_shape_with_path:
                return cluster

    return None


def add_joints_to_skincluster(skinned_mesh, joint=''):
    """Add given joints into given mesh skincluster with locked, zeroed weights

    Arguments:
        joints (list): names of joints to add
        skinned_mesh (string): target skinned geo
    """
    #get skin cluster from skinned mesh
    skin_cluster = mc.ls(mc.listHistory(skinned_mesh), type='skinCluster')

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
    ccu.lock_and_hide(duped_object,
                      lock=False,
                      hide=False,
                      attrs=['tx','ty','tz','rx','ry','rz','sx','sy','sz'])
    mc.makeIdentity(duped_object, apply=True)
    mc.delete(duped_object, constructionHistory=True)

    # hide original object for visual clarity
    mc.hide(selected_object)

    # go to vertex selection mode
    clear_selection()
    mc.select(duped_object)
    mc.selectMode(component=True)
    mc.selectType(vertex=True)

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
