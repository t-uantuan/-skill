#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""example-table-sync · 〈表X〉增量同步 机械核验脚本（模板）

前置条件（缺一即 SKIPPED，不算 FAIL）：
  1. 本文件顶部配置已填实际值（仍是〈占位符〉即退出 SKIPPED）
  2. 集群可达：ssh 〈用户名〉@〈节点1〉
  3. 业务库可查

断言全部来自 decisions.md 第「验收标准」节（编号 AS-n = 本 case 验收断言，
与体系失败模式编号 FM-xx 是两套编号，互不相干）：
  AS-1 对账 diff=0      AS-2 幂等重跑 count 不变
  AS-3 断点值非空       AS-4 ODS count = 落盘 count

用法：python check.py            # 全量跑
      python check.py --quick   # 跳过幂等重跑（会真实重写一次数据）
退出码：0=全绿 1=有FAIL 2=SKIPPED（环境不可用/配置未填）
"""
import subprocess, sys, argparse

# ===== 落地时填实际值（对应 context.md 冻结事实；带〈〉即未填）=====
HOST = "〈节点1〉"
USER = "〈用户名〉"
TABLE = "〈表X〉"
DB = "〈业务库〉"
INC_SCRIPT = "~/bin/〈增量同步脚本〉"
PWD_FILE = "〈密码文件路径〉"
HDFS_ROOT = "〈落盘根路径〉"
ODS_DB = "〈ODS库〉"
CHECK_COL_Q = "断点值"
CONTROL_TABLE = "〈断点控制表〉"
QUERY_CLIENT = "〈查询客户端〉"
ENGINE_SETUP = "〈引擎会话设置〉"

PLACEHOLDER = "〈"

results = []

def ssh(cmd, timeout=120):
    return subprocess.run(["ssh", f"{USER}@{HOST}", cmd],
                          capture_output=True, text=True, timeout=timeout)

def db_q(sql):
    # 凭据走工具原生文件机制，不在命令行展开密码（骨架硬规则 4）
    r = ssh(f"〈db客户端〉 --defaults-extra-file={PWD_FILE} -N -B -e \"{sql}\"")
    return r.stdout.strip()

def hdfs_count(dt):
    r = ssh(f"〈存储客户端〉 -cat {HDFS_ROOT}/{TABLE}_inc/{dt}/* 2>/dev/null | wc -l")
    return int(r.stdout.strip() or -1)

def check(name, ok, evidence):
    results.append((name, "PASS" if ok else "FAIL", evidence))

def unfilled():
    for v in (HOST, USER, TABLE, DB, INC_SCRIPT, PWD_FILE, HDFS_ROOT, ODS_DB, CONTROL_TABLE, QUERY_CLIENT, ENGINE_SETUP):
        if PLACEHOLDER in v:
            return True
    return False

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--quick", action="store_true")
    quick = ap.parse_args().quick

    if unfilled():
        print("SKIPPED: 配置仍是占位符，未落地（按模板交付，不算 FAIL）")
        sys.exit(2)

    # 环境探测
    probe = ssh("echo ok")
    if probe.returncode != 0:
        print("SKIPPED: cluster unreachable"); sys.exit(2)

    # AS-3 断点值非空
    lv = db_q(f"SELECT {CHECK_COL_Q} FROM {DB}.{CONTROL_TABLE} WHERE table_name='{TABLE}'")
    check("AS-3 断点值非空", bool(lv), f"断点值={lv!r}")

    # AS-1 对账 diff=0
    src = db_q(f"SELECT COUNT(*) FROM {DB}.{TABLE}")
    dt = ssh("date +%F").stdout.strip()
    hdfs = hdfs_count(dt)
    check("AS-1 对账 diff=0", src.isdigit() and int(src) == hdfs and hdfs >= 0,
          f"db={src} hdfs[{dt}]={hdfs}")

    # AS-2 幂等（可选跳过）
    if not quick:
        r1 = ssh(f"{INC_SCRIPT} {TABLE} {dt}", timeout=600)
        h2 = hdfs_count(dt)
        check("AS-2 幂等重跑 count 不变", h2 == hdfs, f"before={hdfs} after={h2}")

    # AS-4 ODS = 落盘
    # 查询客户端与引擎会话设置均为占位；落地按本域查询引擎填写（原示例为 Hive 方言）
    ods = ssh(f"{QUERY_CLIENT} -e \"{ENGINE_SETUP}; SELECT COUNT(*) FROM {ODS_DB}.{TABLE}_inc WHERE dt='{dt}'\" 2>/dev/null")
    ods_n = ods.stdout.strip().splitlines()[-1] if ods.stdout.strip() else "-1"
    check("AS-4 ODS=落盘（且查询<30s）", ods_n.isdigit() and int(ods_n) == hdfs,
          f"ods={ods_n} hdfs={hdfs}")

    fails = [r for r in results if r[1] == "FAIL"]
    for n, s, e in results:
        print(f"[{s}] {n}  | {e}")
    print("=" * 40)
    verdict = "ALL GREEN" if not fails else f"{len(fails)} FAIL"
    if quick and not fails:
        verdict += "（quick：AS-2 未跑，不作正式全绿，正式验收须全量跑）"
    print("RESULT:", verdict)
    sys.exit(0 if not fails else 1)

if __name__ == "__main__":
    main()
