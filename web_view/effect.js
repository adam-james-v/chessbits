//this function includes all necessary js files for the application
function include(file)
{

  var script  = document.createElement('script');
  script.src  = file;
  script.type = 'text/javascript';
  script.defer = true;

  document.getElementsByTagName('head').item(0).appendChild(script);

}

/* include any js files here */


function aveffect() {
    // postprocessing
    composer = new THREE.EffectComposer( renderer2 );
    renderPass = new THREE.RenderPass( scene, camera );
    copyPass = new THREE.ShaderPass( THREE.CopyShader );
    composer.addPass( renderPass );

    effectSobel = new THREE.ShaderPass( THREE.SobelOperatorShader );
    effectSobel.uniforms.resolution.value.x = window.innerWidth*4;
    effectSobel.uniforms.resolution.value.y = window.innerHeight*4;
    composer.addPass( effectSobel );

    effectContrast = new THREE.ShaderPass( THREE.BrightnessContrastShader );
    effectContrast.uniforms.brightness.value = 0.5;
    effectContrast.uniforms.contrast.value = 1;
    composer.addPass( effectContrast );

    AlphaPass = new THREE.ShaderPass( THREE.AlphaShader );
    composer.addPass( AlphaPass );

    composer.addPass( copyPass );
    copyPass.renderToScreen = true;
}