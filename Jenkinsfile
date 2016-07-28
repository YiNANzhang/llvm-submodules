node {
  sh 'env'
  def jobScript = env.JENKINS_HOME + '/workspace/' + env.JOB_NAME + '@script/Bots/' + env.JOB_NAME + '.groovy'
  load jobScript
}()
