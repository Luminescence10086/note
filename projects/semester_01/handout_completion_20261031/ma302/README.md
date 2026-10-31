# MA302作者数值验证项目

WSL Ubuntu/GCC，2026-10-31作者运行。编译：gcc -std=c11 -O2 -Wall -Wextra -Werror verify.c -lm -o verify。运行 ./verify 输出validation.txt。python3 plot_svg.py生成logistic_bifurcation.svg，标准库无需第三方依赖。

验证：Euler/RK4精确衰减解；HH常速率教学特例（非1952参数动作电位复现）；Lorenz到T=1步长减半；201个logistic参数×128个保留点，每参数丢弃2000次暂态，初值0.271828。failures=0见validation.txt。数值图不证明无限级联或混沌。

WSL缺matplotlib及ensurepip；bundled Python也缺matplotlib；venv初始化失败，没有安装系统包。不完整.venv目录未作为可用环境，非必要清理被自动审批拒绝而跳过。
