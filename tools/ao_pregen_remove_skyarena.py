"""Exact approved Demi's Sky Arena removal from future CurseForge import manifests.

Does not mutate the original input or change any other projectID/fileID pairs.
Returns new ordered list and count removed. This only changes future imports:
previously generated chunks and saved structures are not retroactively edited.
"""
SKY_ARENA_PROJECT_ID=1141465
SKY_ARENA_FILE_ID=7053645

def omit_demis_sky_arena(files):
    if not isinstance(files,list):raise TypeError("Expected manifest 'files' list")
    matching=[f for f in files if f.get("projectID")==SKY_ARENA_PROJECT_ID]
    if len(matching)>1:raise ValueError("Multiple Sky Arena references, refusing to guess")
    if matching and matching[0].get("fileID")!=SKY_ARENA_FILE_ID:
        raise ValueError("Sky Arena project ID has unexpected file version, review explicitly")
    retained=[dict(x) for x in files if x.get("projectID")!=SKY_ARENA_PROJECT_ID]
    removed=len(files)-len(retained)
    if removed not in (0,1):raise ValueError("Unexpected removal count")
    if len({(x.get("projectID"),x.get("fileID")) for x in retained})!=len(retained):
        raise ValueError("Duplicate CF entries detected")
    return retained,removed
