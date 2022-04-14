import maya.cmds as mc
import maya.api.OpenMaya as om
import pymel.core as pm

def rename_deformers(objects=[]):
    """_summary_

    Args:
        objects (list, optional): _description_. Defaults to [].

    Returns:
        _type_: _description_
    """

    if not objects:
        objects = mc.ls(sl=True)
    if objects:
        for object in objects:
            inputs = mc.listHistory(object, interestLevel=1)
            skin_cluster = mc.ls(inputs, typ='skinCluster')
            if skin_cluster:
                new_skin_cluster = mc.rename(skin_cluster[0], 'skinCluster_{}'.format(object))
    
    #TODO: eval this return
    return new_skin_cluster


def copy_skin_cluster(skinned_mesh, target_mesh=[], rename=True):
    """_summary_

    Args:
        skinned_mesh (_type_): _description_
        target_mesh (list, optional): _description_. Defaults to [].
        rename (bool, optional): _description_. Defaults to True.

    Returns:
        _type_: _description_
    """

    maxInfluences = 0
    maintainMaxInfluences = False
    new_skin_cluster_names = []

    skin_cluster = mc.ls(mc.listHistory(skinned_mesh), type='skinCluster')

    if skin_cluster:
        maintainMaxInfluences = mc.getAttr('{}.maintainMaxInfluences'.format(skin_cluster[0]))
        maxInfluences = mc.getAttr('{}.maxInfluences'.format(skin_cluster[0]))

    for mesh in target_mesh:
        # remove existing skincluster
        old_skin_cluster = mc.ls(mc.listHistory(skinned_mesh), type='skinCluster')
        if old_skin_cluster:
            mc.delete(old_skin_cluster)

        joints = mc.skinCluster(skin_cluster[0], weightedInfluence=True, query=True)

        new_skin_cluster = mc.skinCluster(joints, mesh, toSelectedBones=True)[0]

        mc.setAttr('{}.maintainMaxInfluences'.format(new_skin_cluster),maintainMaxInfluences)
        mc.setAttr('{}.maxInfluences'.format(new_skin_cluster), maxInfluences)

        mc.copySkinWeights(sourceSkin=skin_cluster[0],
                           destinationSkin=new_skin_cluster,
                           notMirror=True,
                           surfaceAssociation='closestPoint')

        if rename:
            new_skin_cluster_name = renameDeformers(objects=[mesh])
        else:
            new_skin_cluster_name = new_skin_cluster
        new_skin_cluster_names.append(new_skin_cluster_name)
    
    # TODO: evaluate this return statement, parenthesis needed?
    return (new_skin_cluster_names)


def copySkinCluster(source='', dest=[], rename=False):
    maxInfluences = 0
    maintainMaxInfluences = False
    if not source and not dest:
        objects = mc.ls(sl=True)
        if len(objects) < 2:
            return False
        else:
            source = objects[0]
            dest = objects[1:]
    sourceHistory = mc.listHistory(source, lv=1)
    sc = mc.ls(sourceHistory, typ='skinCluster')
    if sc:
        maintainMaxInfluences = mc.getAttr('{}.maintainMaxInfluences'.format(
            sc[0]))
        maxInfluences = mc.getAttr('{}.maxInfluences'.format(sc[0]))
    newSCNames = []
    for d in dest:
        destHistory = mc.listHistory(d, lv=1)
        oldSC = mc.ls(destHistory, typ='skinCluster')
        if oldSC:
            mc.delete(oldSC)
        jnts = mc.skinCluster(sc[0], weightedInfluence=True, q=True)
        newSC = mc.skinCluster(jnts, d, tsb=True)[0]
        mc.setAttr('{}.maintainMaxInfluences'.format(newSC),
                   maintainMaxInfluences)
        mc.setAttr('{}.maxInfluences'.format(newSC), maxInfluences)
        mc.copySkinWeights(ss=sc[0],
                           ds=newSC,
                           nm=True,
                           surfaceAssociation='closestPoint')
        if rename:
            pass
            newSCName = renameDeformers(objects=[d])
        else:
            newSCName = newSC
        newSCNames.append(newSCName)
    #mc.select(objects)
    return (newSCNames) 


def add_joints_to_skincluster(skinned_mesh, joints=[]):
    """Add given joints into given mesh skincluster with locked, zeroed weights

    Arguments:
        joints (list): names of joints to add
        skinned_mesh (string): target skinned geo

    Returns:

    """
    skin_cluster = mc.ls(mc.listHistory(skinned_mesh), type='skinCluster')

    for joint in joints:
        mc.skinCluster(skin_cluster, edit=True, lockWeights=True, weight=0, addInfluence=joint)


def duplicate_selected_faces():
    """Creates a duplicate object and deletes faces to create a new object from 
    selected faces. Goal is to not leave history on original object.

    Returns:
        selected_object (string): selected original mesh
        duped_object (string): duplicated face geometry
    """

    # TODO: refactor this to work with button press? and be smarter?
    selected_faces = mc.ls(sl=True)

    selected_object = selected_faces[0].split('.')[0]
    duped_object = mc.duplicate(selected_object)[0]

    keepable_geo = []
    
    for face in selected_faces:
        face = face.replace(selected_object, duped_object)
        keepable_geo.append(face)

    mc.select(clear=True)

    # select faces on duplicate geometry, invert selection, and delete remaining faces
    mc.select(keepable_geo)
    mc.select(duped_object + '.f[*]', toggle=True)
    delete_faces = mc.ls(sl=True)
    mc.delete(delete_faces)

    # clear history on duplicate
    mc.delete(duped_object, constructionHistory=True)

    # TODO: hide original object and isolate new object as part of tool for easy viewing?
    mc.hide(selected_object)

    return selected_object, duped_object


def get_selected_verts():
    """Grab selected verts in an ordered selection list

    Returns:
        verts: list of selected verts
    """
    verts = mc.ls(orderedSelection=True)

    return verts


def clear_selection():
    """Clears selection :)
    """
    mc.select(clear=True)


def create_locs_on_verts(base_geometry):
    """Creates locators on selected verts on given base geometry object

    Returns:
        locs (list): list of duplicated locators
        vert_loc_pairs (dict): dict of locs and matching vert pairs
    """
    # FIXME: save vertex selection data as part of class variable, something accessible? 
   
    verts = get_selected_verts()
    locs = []
    vert_loc_pairs = {}


    for i, vert in enumerate(verts):
        loc = mc.spaceLocator(name='loc_{0}_{1}'.format(base_geometry, i))
        mc.xform(loc,
                 worldSpace=True,
                 translation=mc.xform(vert, query=True, worldSpace=True, translation=True))

        locs.append(loc)
        vert_loc_pairs[vert] = loc

    for loc in locs:
        # align locator to nearest normal
        constraint = mc.normalConstraint(base_geometry, loc, aimVector=(1, 0, 0), worldUpType=0)
        mc.delete(constraint)
    
    return locs, vert_loc_pairs


def get_vertex_uvs():
    """Gets UV coordinates of selected vertex

    Returns:
        uv_coords (dict): dictionary of selected verts and associated UV coordinates
    """
    #FIXME: need unified reference variable for this
    verts = get_selected_verts()

    uv_coords = {}

    for vert in verts:
        mc.select(vert)
        mc.ConvertSelectionToUVs()
        uv_values = mc.polyEditUV(query=True)
        uv_coords[vert] = uv_values

    return uv_coords

# how to mirror this setup across the object? symmetry mode turned on and selected verts from there?






# def get_vtx_transforms(vtx=[]):
#     """_summary_

#     Args:
#         vtx (list, optional): _description_. Defaults to [].
#     """

#     vtx_transforms = []

#     for vt in vtx:
#         point_position = mc.xform(vt, query=True, objectSpace=True, translation=True)
#         vtx_transforms.append(point_position)

#     # want to select verts and get position and normal direction 


# def flatten_selection_list():
#   """
#   save current selection list flattened as tuple
#   """
#   s = mc.ls(sl=True, flatten=True)
#   s = tuple(i for i in s) #type:ignore
#   return s

# # NOTE: Various methods are available to query an MObject's type. If you are
# # unsure of the type of an MObject, use the apiType() method to get the
# # MObject's type. The return value will be a type in MFn::Type. If you want to
# # know if an MObject is compatible with a specific function set, pass the
# # function set type to the hasFn() method.

# tsphere = mc.polySphere(sx=30, sy=30, radius=30)
# mc.select(tsphere)
# selection = om.MGlobal.getActiveSelectionList()

# # getting the 0 idx of selection list get the dagpath and mobject handle
# tdag, tsphere_mobj = selection.getComponent(0) #type:ignore (mdagpath, mobject)

# mfn_sphere = om.MFnMesh(tdag)
# # NOTE: verify the sphere1 tsphere is has the function set applied to it
# # print(mfn_sphere.fullPathName())

# # world space
# ws = om.MSpace.kWorld

# # fn getPoints returns a MPointArray of world positions
# sphere_vtxs_ws = mfn_sphere.getPoints(ws)

# # fn getNormals() returns a MFloatVectorArray
# sphere_normals_ws = mfn_sphere.getNormals(ws)

# YVector = om.MVector(0,1,0)

# mfn_xform = om.MFnTransform(tdag)

# # create an array of mobject references to locators
# loc_mobjs = om.MObjectArray()
# loc_mobjs.setLength(len(sphere_vtxs_ws))

# # create an array of dagpaths to locators
# loc_dags = om.MDagPathArray()

# # clear selection
# clear_select()
# # create the locators aggreating the selection add=True
# for i in range(len(sphere_vtxs_ws)):
#   loc = mc.spaceLocator()
#   mc.select(loc, add=True)
#   loc_sl = om.MGlobal.getActiveSelectionList()
#   ldag, lmobj = loc_sl.getComponent(0)
#   loc_dags.append(ldag)
#   loc_mobjs.append(lmobj)
#   clear_select()


# start = time()
# for i in range(len(sphere_normals_ws)):
#   # ensure its a unit vector
#   normal = sphere_normals_ws[i].normalize()
#   n = om.MVector(normal.x, normal.y, normal.z)
#   quaternion = om.MQuaternion(YVector, n, 1.0)
#   offsetvector = om.MVector(sphere_vtxs_ws[i].x, sphere_vtxs_ws[i].y,
#                             sphere_vtxs_ws[i].z)
#   locMobj = loc_mobjs[i]
#   locdag = loc_dags[i]
#   # initalize a transform function set on the locator dagpath
#   locxform = om.MFnTransform(locdag)
#   # rotate that locator by the quaternoin
#   locxform.rotateBy(quaternion, ws)
#   # offset vector by world position
#   locxform.translateBy(offsetvector, ws)
#   # offset vector by unit normal of vertex
#   #locxform.translateBy(n, ws)
# end = time()
# # 3.189 for 40k locators

