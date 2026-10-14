#!/usr/bin/env python3
"""Generate a repository-local SVG using public GitHub REST data.

Python 3.10+, standard library only. The script never requests private repositories.
An API error leaves the previous card intact. No personal access token is required
in Actions: use the scoped, automatically supplied GITHUB_TOKEN.
"""
from __future__ import annotations
import argparse
from collections import Counter
from datetime import datetime, timezone
import html
import json
import os
from pathlib import Path
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

ROOT=Path(__file__).resolve().parents[1]
API='https://api.github.com'


def get_json(path: str, token: str, retries: int = 2):
    headers={'Accept':'application/vnd.github+json','User-Agent':'local-profile-card','X-GitHub-Api-Version':'2022-11-28'}
    if token:
        headers['Authorization']=f'Bearer {token}'
    request=urllib.request.Request(API+path,headers=headers)
    for attempt in range(retries+1):
        try:
            with urllib.request.urlopen(request,timeout=25) as response:
                return json.load(response)
        except urllib.error.HTTPError as exc:
            if exc.code >= 500 and attempt < retries:
                time.sleep(2**attempt); continue
            # Never output the request headers or token.
            raise RuntimeError(f'GitHub API returned HTTP {exc.code} for {path}. Existing artwork was not changed.') from None
        except (urllib.error.URLError,TimeoutError) as exc:
            if attempt < retries:
                time.sleep(2**attempt); continue
            raise RuntimeError(f'Could not reach the GitHub API for {path}. Existing artwork was not changed.') from None
    raise RuntimeError('GitHub API request did not complete.')


def summarize(profile: dict, repositories: list[dict]) -> dict:
    # Deduplicate defensively: a repo may move between pages during an update.
    unique={r['id']:r for r in repositories if not r.get('private',False)}
    owned=[r for r in unique.values() if not r.get('fork',False)]
    languages=Counter(r['language'] for r in owned if r.get('language'))
    return {
        'username':profile['login'],
        'updated_at':datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC'),
        'original_public_repositories':len(owned),
        'stars_on_original_public_repositories':sum(r.get('stargazers_count',0) for r in owned),
        'followers':profile.get('followers',0),
        'primary_language_counts':dict(languages.most_common(6)),
        'primary_language_repository_count':sum(languages.values()),
        'scope':'Public repositories owned by this account; forks excluded; archived original repositories included. Language chart counts each repository once by its GitHub primary language, not code bytes or proficiency.'
    }


def fetch_summary(username: str, token: str) -> dict:
    profile=get_json('/users/'+urllib.parse.quote(username),token)
    repositories=[]
    for page in range(1,1001):
        batch=get_json(f'/users/{urllib.parse.quote(username)}/repos?type=owner&per_page=100&sort=full_name&page={page}',token)
        if not isinstance(batch,list):
            raise RuntimeError('Unexpected repository response; existing artwork was not changed.')
        repositories.extend(batch)
        if len(batch)<100:
            break
    else:
        raise RuntimeError('Pagination safety limit reached; refusing to publish partial statistics.')
    return summarize(profile,repositories)


def render(data: dict) -> str:
    esc=lambda s:html.escape(str(s),quote=True)
    def text(x,y,s,size=18,color='#EDF5FF',weight=400):
        return f'<text x="{x}" y="{y}" fill="{color}" font-family="Arial, Helvetica, sans-serif" font-size="{size}" font-weight="{weight}">{esc(s)}</text>'
    b=text(32,38,'PUBLIC GITHUB SNAPSHOT',13,'#66E3F1',700)+text(800,38,data['updated_at'],12,'#93A8C1')
    for i,(key,label) in enumerate([
        ('original_public_repositories','Original public repositories'),
        ('stars_on_original_public_repositories','Stars on those repositories'),
        ('followers','Followers')]):
        x=33+i*357
        b+=text(x,115,f"{data[key]:,}",51,'#EDF5FF',700)+text(x,148,label,16,'#93A8C1')
    b+='<path d="M32 174 H1088" stroke="#22344A"/>'
    b+=text(32,206,'PRIMARY LANGUAGES / REPOSITORY COUNTS',12,'#AA9AFF',700)
    lang=list(data['primary_language_counts'].items())
    if lang:
        for i,(name,n) in enumerate(lang):
            x=33+(i%3)*357; y=242+(i//3)*33
            b+=text(x,y,f'{name}: {n}',16,'#EDF5FF')
    else:
        b+=text(33,242,'No primary-language data is available for these repositories.',16,'#93A8C1')
    b+=text(32,312,'Public owned repositories only; forks excluded. Languages count repositories, not proficiency.',12,'#93A8C1')
    b+=text(32,334,'Archived original repositories are included. Snapshot data, not a live contribution graph.',12,'#93A8C1')
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="1120" height="360" viewBox="0 0 1120 360" role="img"><title>{esc(data["username"])} public GitHub statistics, {esc(data["updated_at"])}</title><rect x=".5" y=".5" width="1119" height="359" rx="24" fill="#080D18" stroke="#22344A"/>{b}</svg>\n'


def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--username',default=os.getenv('PROFILE_USERNAME','Geethanjana99'))
    parser.add_argument('--output',type=Path,default=ROOT/'assets/github-activity.svg')
    args=parser.parse_args()
    if not re.fullmatch(r'[A-Za-z0-9](?:[A-Za-z0-9-]{0,38})',args.username):
        parser.error('Invalid GitHub username.')
    try:
        data=fetch_summary(args.username,os.getenv('GITHUB_TOKEN',''))
        svg=render(data)
        args.output.parent.mkdir(parents=True,exist_ok=True)
        tmp=args.output.with_suffix('.svg.tmp')
        tmp.write_text(svg,encoding='utf-8')
        tmp.replace(args.output)
        print(f'Updated {args.output.name} from public GitHub data.')
        return 0
    except (RuntimeError,ValueError,KeyError,OSError) as exc:
        print(f'ERROR: {exc}',file=sys.stderr)
        return 1

if __name__=='__main__':
    raise SystemExit(main())
