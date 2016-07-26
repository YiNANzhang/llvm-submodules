node {
  stage 'Checkout'
  git url:'git@github.com:llvm-beanz/llvm-submodules.git', credentialsId:'0091ce79-f8af-4e94-a1ca-1d48a35c06d3'
  stage 'Submodule Update'
  sh '$PWD/scripts/update-repo.sh'
}
