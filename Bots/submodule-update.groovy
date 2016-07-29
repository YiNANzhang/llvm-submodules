{ ->
  node {
    stage 'Checkout'
    checkout([$class: 'GitSCM', branches: [[name: 'origin/master']], doGenerateSubmoduleConfigurations: false, extensions: [[$class: 'SubmoduleOption', disableSubmodules: false, recursiveSubmodules: true, trackingSubmodules: true, reference: '', timeout: 1000]], submoduleCfg: [], userRemoteConfigs: [[url: 'github.com:llvm-beanz/llvm-submodules.git', name: 'origin', credentialsId: '0091ce79-f8af-4e94-a1ca-1d48a35c06d3']]])
    stage 'Submodule Update'
    sh '(git commit -a -m "Submodule update $(expr $(git rev-list --count HEAD) + 1)" && git push git@github.com:llvm-beanz/llvm-submodules.git HEAD:master) || true'
  }
}
