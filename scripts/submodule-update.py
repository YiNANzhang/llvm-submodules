#!/usr/bin/env python

import os
import subprocess
import tempfile

def getSubmoduleStatus():
  output = subprocess.check_output(['git', 'submodule', 'status'])
  module_status = {}
  for line in output.split("\n"):
    line_parts = line.split(" ")
    if len(line_parts) > 1:
      commit_hash = line_parts[1]
      module = line_parts[2]
      module_status[module] = commit_hash
  return module_status

def getCommitsSinceUpdate(submodule, last_hash):
  subprocess.check_call(['git', '--git-dir=%s/%s/.git' % (os.getcwd(), submodule), 'fetch', 'origin', 'master'])
  hashes = subprocess.check_output(['git', '--git-dir=%s/%s/.git' % (os.getcwd(), submodule), 'log', '--pretty=%H', '%s..origin/master' % last_hash])
  return hashes.split("\n")[:-1]

def getTimeOfCommit(submodle, commit_hash):
  timestamp = subprocess.check_output(['git', '--git-dir=%s/%s/.git' % (os.getcwd(), submodule), 'log', '--pretty=%cI', commit_hash])
  return timestamp

submodule_status = getSubmoduleStatus()
new_commits = {}
for submodule, commit_hash in submodule_status.iteritems():
  new_commits[submodule] = getCommitsSinceUpdate(submodule, commit_hash)

while len(new_commits) > 0:
  to_remove = []
  oldest_commit = None
  oldest_commit_time = None
  oldest_commit_module = None
  for submodule in new_commits:
    if len(new_commits[submodule]) == 0:
      to_remove.extend(submodule)
      continue
    if oldest_commit is None:
      oldest_commit = new_commits[submodule][0]
      oldest_commit_time = getTimeOfCommit(submodule, oldest_commit)
      oldest_commit_module = submodule
    else:
      commit = new_commits[submodule][0]
      commit_time = getTimeOfCommit(submodule, commit)
      if commit_time < oldest_commit:
        oldest_commit = commit
        oldest_commit_time = commit_time
        oldest_commit_module = submodule
  if oldest_commit:
    git_dir_flag = '--git-dir=%s/%s/.git' % (os.getcwd(), oldest_commit_module)
    subprocess.check_call(['git', git_dir_flag, 'checkout', oldest_commit])
    commit_message = subprocess.check_output(['git', git_dir_flag, 'log', '-n', '1', '--pretty=%B', oldest_commit])
    commit_author = subprocess.check_output(['git', git_dir_flag, 'log', '-n', '1', '--pretty=%an <%ae>', oldest_commit]).strip()
    temp = tempfile.NamedTemporaryFile(delete=False)
    temp.write(commit_message)
    temp.close()

    subprocess.check_call(['git', 'add', oldest_commit_module])
    subprocess.check_call(['git', 'commit', '--author=%s' % commit_author, '--file=%s' % temp.name])
    os.unlink(temp.name)

  # remove empty entries
  for submodule in to_remove:
    new_commits.pop(submodule, None)

