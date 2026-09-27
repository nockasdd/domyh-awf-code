"""Test the UE Native Python HTTP Server on port 30011 - output to file"""
import urllib.request
import json
import base64
import sys

TESTS = [
    {
        "name": "1. Basic Hello World",
        "code": 'import unreal\nunreal.log("Hello from test script!")\nprint("OK - Basic test passed")'
    },
    {
        "name": "2. List Level Actors",
        "code": 'import unreal\nactors = unreal.EditorLevelLibrary.get_all_level_actors()\nprint(f"Total actors: {len(actors)}")\nfor a in actors[:10]:\n    print(f"  - {a.get_name()} ({a.get_class().get_name()})")'
    },
    {
        "name": "3. Get Project Info",
        "code": 'import unreal\nproject_dir = unreal.Paths.project_dir()\nprint(f"Project Dir: {project_dir}")'
    },
    {
        "name": "4. Spawn a PointLight Actor",
        "code": 'import unreal\nlight = unreal.EditorLevelLibrary.spawn_actor_from_class(unreal.PointLight, unreal.Vector(0, 0, 300))\nif light:\n    light.set_actor_label("HSA_TestLight")\n    print(f"Spawned: {light.get_name()} at (0,0,300)")\nelse:\n    print("ERROR: Failed to spawn actor")'
    },
    {
        "name": "5. Search Assets (fixed)",
        "code": 'import unreal\nar = unreal.AssetRegistryHelpers.get_asset_registry()\nassets = ar.get_assets_by_path("/Game", recursive=True)\nprint(f"Found {len(assets)} assets in /Game")\nfor a in assets[:5]:\n    print(f"  - {a.asset_name}")'
    },
]

def run_test(name, code):
    code_b64 = base64.b64encode(code.encode("utf-8")).decode("utf-8")
    data = json.dumps({"code_base64": code_b64}).encode("utf-8")
    req = urllib.request.Request(
        "http://127.0.0.1:30011/execute",
        data=data,
        headers={"Content-Type": "application/json"}
    )
    try:
        resp = urllib.request.urlopen(req, timeout=15)
        result = json.loads(resp.read().decode("utf-8"))
        status = "PASS" if result.get("ok") else "FAIL"
        output = f"\n{'='*60}\n[{status}] {name}\n{'='*60}\n"
        if result.get("output"):
            output += f"Output:\n{result['output']}\n"
        if result.get("error"):
            output += f"Error:\n{result['error']}\n"
        print(output)
        return result.get("ok", False), output
    except Exception as e:
        output = f"\n{'='*60}\n[ERROR] {name}\n{'='*60}\nException: {e}\n"
        print(output)
        return False, output

if __name__ == "__main__":
    header = "=" * 60 + "\nUE5 Native Python HTTP Server - Test Suite\nTarget: http://127.0.0.1:30011\n" + "=" * 60
    print(header)
    
    all_output = [header]
    passed = 0
    total = len(TESTS)
    
    for t in TESTS:
        ok, out = run_test(t["name"], t["code"])
        all_output.append(out)
        if ok:
            passed += 1
    
    summary = f"\n{'='*60}\nRESULTS: {passed}/{total} tests passed\n{'='*60}"
    print(summary)
    all_output.append(summary)
    
    with open("test_results.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(all_output))
    
    print(f"\nFull results saved to test_results.txt")
