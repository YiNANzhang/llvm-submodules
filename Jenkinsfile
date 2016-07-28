node {
  stage 'Checkout'
  dir('src') {
    checkout([$class: 'GitSCM', branches: [[name: 'origin/master']], doGenerateSubmoduleConfigurations: false, extensions: [[$class: 'PreBuildMerge', options: [$class: 'UserMergeOptions', mergeRemote: 'origin', mergeTarget: 'FreeBSD-RA-x86_64', mergeStrategy: 'default', fastForwardMode: 'FF']]], submoduleCfg: [], userRemoteConfigs: [[url: 'github.com:llvm-beanz/llvm-submodules.git', name: 'origin', credentialsId: '0091ce79-f8af-4e94-a1ca-1d48a35c06d3']]])
    stage 'Submodule Update'
    sh 'git submodule init && git submodule update'

    sh 'env'

    dir('build') {
      stage 'Configure'
      sh 'cmake -G Ninja -DCMAKE_CXX_COMPILER=clang++37 -DCMAKE_C_COMPILER=clang37 -C ../cmake-caches/FreeBSD-RA-x86_64.cmake -DLLVM_EXTERNAL_CLANG_SOURCE_DIR=../clang -DLLVM_EXTERNAL_LLD_SOURCE_DIR=../lld -DLLVM_EXTERNAL_CLANG_TOOLS_EXTRA_SOURCE_DIR=../clang-tools-extra -DLLVM_EXTERNAL_COMPILER_RT_SOURCE_DIR=../compiler-rt ../llvm'

      stage 'Build'
      sh 'ninja'

      stage 'check-llvm'
      sh 'ninja check-llvm || true'

      stage 'check-clang'
      sh 'ninja check-clang || true'

      stage 'check-lld'
      sh 'ninja check-lld || true'

      stage 'archive results'
      step([$class: 'JUnitResultArchiver', testResults: '**/testresults.xunit.xml'])

    }

    stage 'Push'
    if(currentBuild.result == null) {
      sh 'git push git@github.com:llvm-beanz/llvm-submodules.git origin HEAD:FreeBSD-RA-x86_64'
    } else {
      echo 'Skipping push due to failures.'
    }
  }
}

node {
  if(currentBuild.result != null) {
    mail to: 'chris.bieneman@me.com', subject: 'Beanz-Bot: ${env.JOB_NAME} ${currentBuild.result}', body: 'See: ${env.JOB_URL}'
  }
}
