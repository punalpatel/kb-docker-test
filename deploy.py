import requests, os, sys, subprocess
import frontmatter, git, json, markdown2

# https://gitpython.readthedocs.io/en/stable/tutorial.html#the-commit-object

# Set the request parameters
kb_target_url = os.environ['KB_TARGET_URL']
# An example
# export KB_TARGET_URL='https://discuss13420948029.zendesk.com/api/v2/%s'
user = os.environ['KB_USER']  + '/token'
pwd = os.environ['KB_PASSWORD']

# @TODO exclude README.md files

def get_article(article_id):
    """
      Args:
      param1 (int): The first parameter.
      param2 (str): The second parameter.

    Returns:
      bool: The return value. True for success, False otherwise.
    """
    # Check if the article ID exists
    print 'Load an Article -> get_article()'

    try:
        # https://developer.zendesk.com/rest_api/docs/help_center/articles#show-article
        article_url = 'help_center/en-us/articles/%d.json' % (article_id)
        hc_article = zd_request(article_url)    # Check if article_id exists in the Help Center
        if 'id' in hc_article['article'].keys():
            print 'Success - An article exists with ID - %d -> get_article()' % (hc_article['article']['id'])
            return hc_article
        else:
            print 'Error - Unable find an article with ID - %d' % (article_id)
            return False
    except Exception as e:
        pass

def create_article(metadata, content, file_path):
    """
    Args:
      article (article): An instance of a Help Center Article

    Returns:
      article: An instance of a new Help Center Article.
    """
    # POST /api/v2/help_center/sections/{id}/articles.json
    # POST /api/v2/help_center/{locale}/sections/{id}/articles.json
    create_url = 'help_center/en-us/sections/202922587/articles.json'
    # Create a new article
    # @TODO define a section
    html = markdown2.markdown(content)
    data = {'article':{'body': html, 'title': metadata['title'], 'locale': 'en-us'}}
    new_article = zd_request(create_url, data, 'POST')
    # Check if article_id exists in .md
    if new_article:
        print 'Success - An article was created in the helpcenter ' 
        print new_article
        # @TODO - update_git_article
        #update_git_article(new_article, file_path)
        setenv_new_article(new_article, file_path)
    else:
        print 'Error - Unable to create a new article in the helpcenter'

    return new_article


def update_article(metadata, content):
    """
    Args:
      article (article): An instance of a Help Center Article

    Returns:
      article: An instance of the updated Help Center Article.
    """
    print 'Check if article_id exists in the Help Center -> update_article()'
    # Check if the article exists in the helpcenter
    hc_article = get_article(metadata['id'])
    # if the article exists in the helpcenter then updat
    print "here we are"
    if hc_article:
        print 'Success - An article exists with ID - %d -> update_article()' % metadata['id']

        update_url = 'help_center/articles/%d/translations/en-us' %  metadata['id']
        # @TODO define a section
        html = markdown2.markdown(content)
        data = {'translation':{'body': html, 'titie': metadata['title']}}

        updated_article = zd_request(update_url, data, 'PUT')

        if updated_article:
            print 'Success - An article was updated with ID'
            print updated_article
        else:
            print 'Error - Unable to update article'

    # @TODO should we create one anyway? Discuss?
    print "Return an instance of the updated_article -> update_article()"
    return hc_article

def setenv_new_article(article, file_path):
    """
    # Set new article id as environment variable NEW_ARTICLE_ID
    Returns:
      bool: The return value. True for success, False otherwise.
    """
    os.environ["NEW_ARTICLE_ID"]: = article['article']['id']
    return True

def update_git_article(article, file_path):
    """
    # Check if ZD_ID exists
    # if not, append it to the front matter
    # if so set it to the new ZD_ID from create_article
    # Create a new commit on the PR branch
    # Merge the new commit to master \
    # (This could happen as part of the GH merge && check for conflicts?)

    Returns:
      bool: The return value. True for success, False otherwise.
    """
    #file_path='tests/fixtures/article_without_id.md'
    print "File path variable is " + file_path
    new_id = article['article']['id']
    regex = ("s/id:$/id:%s/" % new_id)
    commands = "\n" + "sed -i -e " + regex + " " + file_path + "\n"
    #Command sed
    
    process = subprocess.Popen('/bin/bash', stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    out, err = process.communicate(commands.encode('utf-8'))
    print(out.decode('utf-8'))
    
    # Check the status of the changes
    git_config_email_command = ['git', 'config', '--global', 'user.email', 'travis@travis-ci.org'	
    subprocess.Popen(git_config_email_command).communicate(input=None)
    
    # Check the status of the changes
    git_config_name_command = ['git', 'config', '--global', 'user.name', 'Travis CI']
    subprocess.Popen(git_config_name_command).communicate(input=None)
    
    # Check the status of the changes
    git_remote_command = ['git', 'remote', 'add', 'origin', ' -t kbs', 'https://github.com/pivotal-gss/kb-docker.git']
    subprocess.Popen(git_remote_command).communicate(input=None)
			
    # Check the status of the changes				
    git_push_command = ['git', 'push', '--quiet', '--set-upstream', 'origin', 'kbs']
    subprocess.Popen(git_push_command).communicate(input=None)
						
    # Check the status of the changes
    git_checkout_command = ['git', 'checkout', '-b', 'kbs']
    subprocess.Popen(git_checkout_command).communicate(input=None)

    # Check the status of the changes
    git_status_command = ['git', 'status']
    subprocess.Popen(git_status_command).communicate(input=None)
			
    # Check the status of the change	
    git_add_command = ['git', 'add', '.']
    subprocess.Popen(git_add_command).communicate(input=None)

    # Commit the changes
    git_commit_command = ['git', 'commit', '-m', 'Committing changes $TRAVIS_BUILD_NUMBER - [ci skip] ']
    subprocess.Popen(git_commit_command).communicate(input=None)

    return True


def git_diff(branch1, branch2):
    """
      Args:
      param1 (int): The first parameter.
      param2 (str): The second parameter.

    Returns:
      bool: The return value. True for success, False otherwise.
    """
    repository = git.Git('./')
    log_format = '--name-only'
    commits = []
    # This should use the class variables
    # d = self.repository.diff('%s..%s' % ('master', 'HEAD'), log_format).split("\n")
    try:
        differ = repository.diff('%s..%s' % ('HEAD^'), log_format).split("\n")
        for line in differ:
            if len(line):
                commits.append(line)
    except Exception:
        print 'Please make sure you have a valid repo'
        pass

    #for commit in commits:
    #    print '*%s' % (commit)
    return commits

def zd_request(u, req_data=None, method='GET', ):
    """
      Args:
      method (str): The first parameter.
      data (str): The second parameter.

    Returns:
      bool: The return value. True for success, False otherwise.
    """

    # Package the data in a dictionary matching the expected JSON
    #req_data = {'article': {'title': 'if the article exists in the helpcenter then update'}}
    print req_data
    #content = {'ticket': {'comment': {'body':data}}}

    # Encode the data to create a JSON payload
    payload = json.dumps(req_data)
    headers = {'Content-type': 'application/json'}

    # URL
    print 'Perform an HTTP Request to Zendesk -> zd_request()'
    req_url = '%s/%s' % (kb_target_url, u)
    print req_url

    if method is 'POST':
        print "You trying to POST bro?"
        response = requests.post(req_url, data=payload, auth=(user, pwd), headers=headers)
    elif method is 'PUT':
        print "You trying to PUT bro?"
        print payload
        response = requests.put(req_url, data=payload, auth=(user, pwd), headers=headers)
    else:
        print "You trying to GET bro?"
        response = requests.get(req_url, auth=(user, pwd))

    # Do the HTTP get request
    #response = requests.get(req_url, auth=(user, pwd))
    # Check for HTTP codes other than 200
    if response.status_code != 200:
        print('Status:', response.status_code, 'Problem with the request. Exiting.')

    print response

    # Decode the JSON response into a dictionary and use the data
    data = response.json()

    # print data
    return data

def process_article(metadata, content, file_path):
    """
      Args:
      param2 (str): The second parameter.

    Returns:
      bool: The return value. True for success, False otherwise.
    """
    # TODO loop through diff for .md files (Exclude README.md)
    # Load the markdown from the article
    #article = frontmatter.load('tests/fixtures/barebones.md')
    #article = frontmatter.load('tests/article_without_id.md')

    #print metadata.content
    # return
    # Extract the Article id
    if 'id' in metadata.keys():
        if metadata['id']:
            print 'I HAVE AND ID -> process_article()'
            update_article(metadata, content)
        else:
            print 'NO ID FOR YOU -> process_article()'
            create_article(metadata, content, file_path)

def main():
    """
    """
    # Validate all the files in commit
    # kb_validator = KBValidator()

    # List the files that are different between HEAD..master
    # diff_files = kb_validator.git_diff()
    diff_files = git_diff('master', 'HEAD^')
    print diff_files

    # Loop through the files
    for c in diff_files:
        print '-- ' + c
        # Validate the file is markdown
        if c.endswith(('.md', '.markdown')):
            print '---> ' + c + ' - is markdown: Processing...'
            # article = metadata, content = frontmatter.parse(c.read())

            try:
                with open(c) as f:
                    metadata, content = frontmatter.parse(f.read())
            except IOError:
                # If the diff is a delete or move the file may no longer
                # exist in the current branch
                print 'This file does not exist in the current branch - has title'
                pass

            process_article(metadata, content, c)
        else:
            print '---> ' + c + ' - is not markdown: Skipping'

    """if markup.is_valid:
        print "\n*************************\n"
        print "Failed: %d errors Detected" % markup.is_valid
        print "\n************************\n"
        exit()
    """

if __name__ == "__main__":

    if len(sys.argv) > 1:
        file_name = str(sys.argv[1])
        print file_name
        exit
        if file_name.endswith(('.md', '.markdown')):
            print file_name + ' - is markdown: Processing'
            try:
                with open(file_name) as c:
                    metadata, content = frontmatter.parse(c.read())
            except IOError:
                # If the diff is a delete or move the file may no longer
                # exist in the current branch
                print 'This file does not exist in the current branch - has title'
                pass

            process_article(metadata, content, file_name)
        else:
            print file_name + ' - is not markdown: Skipping'

    else:
        print 'No file specified. \nExample Command:'
        print '\n python scripts/frontmatter-test.py article.md'
        print '*****************************\n'
        print 'Trying to run - main() as fallback'
