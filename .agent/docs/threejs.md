---
library: threejs
version: latest
latest: true
category: 3d-graphics
official_docs: https://threejs.org/docs/
last_updated: 2026-03-21
source: auto-fetched from github-dir
source_url: https://api.github.com/repos/mrdoob/three.js/contents/manual/en
---

# Material Count: 2

newmtl Material
Ns 0.000000
Ka 1.000000 1.000000 1.000000
Kd 0.800000 0.800000 0.800000
Ks 0.000000 0.000000 0.000000
Ke 0.000000 0.000000 0.000000
Ni 1.000000
d 1.000000
illum 1
map_Kd windmill_001_lopatky_COL.jpg
map_Bump windmill_001_lopatky_NOR.jpg

newmtl windmill
Ns 0.000000
Ka 1.000000 1.000000 1.000000
Kd 0.800000 0.800000 0.800000
Ks 0.000000 0.000000 0.000000
Ke 0.000000 0.000000 0.000000
Ni 1.000000
d 1.000000
illum 1
map_Kd windmill_001_base_COL.jpg
map_Bump windmill_001_base_NOR.jpg
map_Ns windmill_001_base_SPEC.jpg
</pre>
<p>We can see there are 2 materials referencing 5 jpg textures
but where are the texture files?</p>
<div class="threejs_center"><img style="width: 757px;" src="../resources/images/windmill-exported-files.png"></div>

<p>All we got was an .OBJ file and an .MTL file.</p>
<p>At least for this model it turns out the textures are embedded
in the .blend file we downloaded. We can ask blender to
export those files to by picking <strong>File-&gt;External Data-&gt;Unpack All Into Files</strong></p>
<div class="threejs_center"><img style="width: 828px;" src="../resources/images/windmill-export-textures.jpg"></div>

<p>and then choosing <strong>Write Files to Current Directory</strong></p>
<div class="threejs_center"><img style="width: 828px;" src="../resources/images/windmill-overwrite.jpg"></div>

<p>This ends up writing the files in the same folder as the .blend file
in a sub folder called <strong>textures</strong>.</p>
<div class="threejs_center"><img style="width: 758px;" src="../resources/images/windmill-exported-texture-files.png"></div>

<p>I copied those textures into the same folder I exported the .OBJ
file to.</p>
<div class="threejs_center"><img style="width: 757px;" src="../resources/images/windmill-exported-files-with-textures.png"></div>

<p>Now that we have the textures available we can load the .MTL file.</p>
<p>First we need to include the <a href="/docs/#examples/loaders/MTLLoader"><code class="notranslate" translate="no">MTLLoader</code></a>;</p>
<pre class="prettyprint showlinemods notranslate lang-js" translate="no">import * as THREE from 'three';
import {OrbitControls} from 'three/addons/controls/OrbitControls.js';
import {OBJLoader} from 'three/addons/loaders/OBJLoader.js';
+import {MTLLoader} from 'three/addons/loaders/MTLLoader.js';
</pre>
<p>Then we first load the .MTL file. When it's finished loading we add
the just loaded materials on to the <a href="/docs/#examples/loaders/OBJLoader"><code class="notranslate" translate="no">OBJLoader</code></a> itself via the <code class="notranslate" translate="no">setMaterials</code>
and then load the .OBJ file.</p>
<pre class="prettyprint showlinemods notranslate lang-js" translate="no">{
+  const mtlLoader = new MTLLoader();
+  mtlLoader.load('resources/models/windmill/windmill.mtl', (mtl) =&gt; {
+    mtl.preload();
+    objLoader.setMaterials(mtl);
    objLoader.load('resources/models/windmill/windmill.obj', (root) =&gt; {
      scene.add(root);
    });
+  });
}
</pre>
<p>And if we try that...</p>
<p></p><div translate="no" class="threejs_example_container notranslate">
  <div><iframe class="threejs_example notranslate" translate="no" style=" " src="/manual/examples/resources/editor.html?url=/manual/examples/load-obj-materials.html"></iframe></div>
  <a class="threejs_center" href="/manual/examples/load-obj-materials.html" target="_blank">click here to open in a separate window</a>
</div>

<p></p>
<p>Note that if we spin the model around you'll see the windmill cloth
disappears</p>
<div class="threejs_center"><img style="width: 528px;" src="../resources/images/windmill-missing-cloth.jpg"></div>

<p>We need the material on the blades to be double sided, something
we went over in <a href="materials.html">the article on materials</a>.
There is no easy way to fix this in the .MTL file. Off the top of my
head I can think of 3 ways to fix this.</p>
<ol>
<li><p>Loop over all the materials after loading them and set them all to double sided.</p>
<pre class="prettyprint showlinemods notranslate notranslate" translate="no"> const mtlLoader = new MTLLoader();
 mtlLoader.load('resources/models/windmill/windmill.mtl', (mtl) =&gt; {
   mtl.preload();
   for (const material of Object.values(mtl.materials)) {
     material.side = THREE.DoubleSide;
   }
   ...
</pre><p>This solution works but ideally we only want materials that need
to be double sided to be double sided because drawing double sided
is slower than single sided.</p>
</li>
<li><p>Manually set a specific material</p>
<p>Looking in the .MTL file there are 2 materials. One called <code class="notranslate" translate="no">"windmill"</code>
and the other called <code class="notranslate" translate="no">"Material"</code>. Through trial and error I figured
out the blades use the material called <code class="notranslate" translate="no">"Material"</code>so we could set
that one specifically </p>
<pre class="prettyprint showlinemods notranslate notranslate" translate="no"> const mtlLoader = new MTLLoader();
 mtlLoader.load('resources/models/windmill/windmill.mtl', (mtl) =&gt; {
   mtl.preload();
   mtl.materials.Material.side = THREE.DoubleSide;
   ...
</pre></li>
<li><p>Realizing that the .MTL file is limited we could just not use it
and instead create materials ourselves.</p>
<p>In this case we'd need to look up the <a href="/docs/#api/en/objects/Mesh"><code class="notranslate" translate="no">Mesh</code></a> object after
loading the obj file.</p>
<pre class="prettyprint showlinemods notranslate notranslate" translate="no"> objLoader.load('resources/models/windmill/windmill.obj', (root) =&gt; {
   const materials = {
     Material: new THREE.MeshPhongMaterial({...}),
     windmill: new THREE.MeshPhongMaterial({...}),
   };
   root.traverse(node =&gt; {
     const material = materials[node.material?.name];
     if (material) {
       node.material = material;
     }
   })
   scene.add(root);
 });
</pre></li>
</ol>
<p>Which one you pick is up to you. 1 is easiest. 3 is most flexible.
2 somewhere in between. For now I'll pick 2.</p>
<p>And with that change you should still see the cloth on the blades
when looking from behind but there's one more issue. If we zoom in close
we see things are turning blocky.</p>
<div class="threejs_center"><img style="width: 700px;" src="../resources/images/windmill-blocky.jpg"></div>

<p>What's going on?</p>
<p>Looking at the textures there are 2 textures labelled NOR for NORmal map.
And looking at them they look like normal maps. Normal maps are generally
purple where as bump maps are black and white. Normal maps represent
the direction of the surface where as bump maps represent the height of
the surface.</p>
<div class="threejs_center"><img style="width: 256px;" src="../examples/resources/models/windmill/windmill_001_base_NOR.jpg"></div>

<p>Looking at <a href="https://github.com/mrdoob/three.js/blob/1a560a3426e24bbfc9ca1f5fb0dfb4c727d59046/examples/js/loaders/MTLLoader.js#L432">the source for the MTLLoader</a>
it expects the keyword <code class="notranslate" translate="no">norm</code> for normal maps so let's edit the .MTL file</p>
<pre class="prettyprint showlinemods notranslate lang-mtl" translate="no"># Blender MTL File: 'windmill_001.blend'
