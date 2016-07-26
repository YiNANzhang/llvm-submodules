node {
  stage 'Checkout'
  git url:'git@github.com:llvm-beanz/llvm-submodule.git', credentialsId:'0091ce79-f8af-4e94-a1ca-1d48a35c06d3'
  stage 'Submodule Update'
  sh 'scripts/update-repo.sh'
}
