from git import Repo

def get_current_branch(request):
    local_repo = Repo(path='../')
    local_branch = local_repo.active_branch.name       
    return {'git_branch': local_branch}