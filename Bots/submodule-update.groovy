{ ->
  node {
    stage 'Checkout'
    checkout([$class: 'GitSCM', branches: [[name: 'origin/master']], doGenerateSubmoduleConfigurations: false, extensions: [], submoduleCfg: [], userRemoteConfigs: [[url: 'github.com:llvm-beanz/llvm-submodules.git', name: 'origin', credentialsId: '0091ce79-f8af-4e94-a1ca-1d48a35c06d3']]])
    sh 'git submodule init'
    sh 'git submodule update'
    stage 'Submodule Update'
    sh 'scripts/submodule-update.py'
    sh 'git push git@github.com:llvm-beanz/llvm-submodules.git HEAD:master || true'
  }
}
