"""Replay the two admission queues. Print a deterministic observation to stdout."""
from collections import deque
import json
from statistics import mean


def size(job):
    return (1, 3, 2, 2)[job % 4]


def evidence(job, index):
    return not (job % 4 == 3 and index == size(job) - 1)


class TaskQueue:
    def __init__(self):
        self.pending = deque()
        self.progress = {}
        self.writes = 0

    def admit(self, job):
        self.pending.append(job)
        self.progress[job] = 0
        self.writes += 1

    def check(self):
        job = self.pending[0]
        index = self.progress[job]
        ok = evidence(job, index)
        self.progress[job] += 1
        self.writes += 1
        done = not ok or self.progress[job] == size(job)
        if done:
            self.pending.popleft()
        return job, index, ok, done


class ObligationQueue:
    def __init__(self):
        self.pending = deque()
        self.results = {}
        self.writes = 0

    def admit(self, job):
        for index in range(size(job)):
            key = job, index
            self.pending.append(key)
            self.results[key] = None
            self.writes += 1

    def check(self):
        job, index = self.pending.popleft()
        ok = evidence(job, index)
        self.results[job, index] = ok
        self.writes += 1
        done = not ok or all(self.results[job, i] is not None for i in range(size(job)))
        return job, index, ok, done


def supported(job, observations):
    return observations == {i: True for i in range(size(job))} and all(
        evidence(job, i) for i in range(size(job))
    )


def snapshot(tick, rate, checks, verdicts, writes):
    jobs = []
    for job, observed in checks.items():
        verdict, end = verdicts.get(job, ('pending', tick))
        jobs.append(dict(job=job, arrival=job // rate, verdict=verdict, checks=observed,
                         wait_or_age=end-job//rate, remaining=size(job)-len(observed),
                         unsupported=verdict == 'accepted' and not supported(job, observed)))
    finished = [r['wait_or_age'] for r in jobs if r['verdict'] != 'pending']
    ages = [r['wait_or_age'] for r in jobs if r['verdict'] == 'pending']
    return dict(tick=tick, arrivals=len(jobs), verified=sum(r['verdict']=='accepted' and not r['unsupported'] for r in jobs),
                unsupported=sum(r['unsupported'] for r in jobs), rejected=sum(r['verdict']=='rejected' for r in jobs),
                unresolved_checks=sum(r['remaining'] for r in jobs), mean_finished_wait=mean(finished),
                max_pending_age=max(ages, default=None), writes=writes, jobs=jobs)


def run(queue, rate):
    checks, verdicts, snapshots = {}, {}, {}
    tick = 0
    while True:
        for job in range(tick * rate, min((tick+1)*rate, 32)):
            queue.admit(job)
            checks[job] = {}
        for _ in range(4):
            if not queue.pending:
                break
            job, index, ok, done = queue.check()
            assert index not in checks[job]
            checks[job][index] = ok
            if done:
                verdicts[job] = ('accepted' if ok else 'rejected', tick)
        for key, active in [('tick_15', tick == 15), ('last_arrival', tick == 31//rate),
                            ('drain', len(verdicts) == 32)]:
            if active:
                # Freeze the observations; later ticks mutate the per-task dictionaries.
                snapshots[key] = json.loads(json.dumps(snapshot(tick, rate, checks, verdicts, queue.writes)))
        if len(snapshots) == 3:
            return snapshots
        tick += 1


if __name__ == '__main__':
    assert not supported(1, {0: True}) and not supported(3, {0: True, 1: True})
    results = {}
    for rate in [1, 2, 4]:
        results[rate] = {}
        for kind in [TaskQueue, ObligationQueue]:
            reports = run(kind(), rate)
            for report in reports.values():
                assert sum(size(row['job']) for row in report['jobs']) == report['unresolved_checks'] + sum(
                    len(row['checks']) for row in report['jobs'])
                assert sum(len(row['checks']) for row in report['jobs']) <= 4*(report['tick']+1)
            assert reports['drain']['arrivals'] == 32 and reports['drain']['unresolved_checks'] == 0
            results[rate][kind.__name__] = reports
    print(json.dumps(results, indent=2))
