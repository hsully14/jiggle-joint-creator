import maya.cmds as mc


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

    return selected_object, duped_object


def get_vtx_transform(vtx=[]):
    """_summary_

    Args:
        vtx (list, optional): _description_. Defaults to [].
    """
    pass

    point_position = mc.xform('pCylinder1.vtx[28]', q=True, objectSpace=True, t=True)

# want to select verts and get position and normal direction 