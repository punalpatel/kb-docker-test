import frontmatter, pytest, sys, subprocess, git

class KBDockerValidator():
    
    repository = git.Git('./')
    base_branch = ''
    target_branch = ''
    is_valid = False

    def __init__(self, ):
        self.set_base()
        self.set_tartget()
        self.repository.branch = 'foo'

    def git_diff(self, branch1='', branch2=''):
        if branch1:
            self.set_base(branch1)
        if branch2:
            self.set_tartget(branch2)

        format = '--name-only'
        commits = []
        # This should use the class variables x
        d = self.repository.diff('%s..%s' % ('HEAD^','prod'), format).split("\n")
        
        return d

    def set_base(self, base='HEAD'):
        if base:
            self.base_branch = base

        self.base_branch = self.repository.active_branch

    def set_tartget(self, target='master'):
        if target:
            self.target_branch = target

        self.target_branch = target

    def validate(self):
        return self.is_valid
