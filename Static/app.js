let pyodide=null;
async function setup(){
    const btn =document.getElementById("simulate-btn")
    const display=document.getElementById("display-plot")
    btn.disabled=true;
    display.textContent="Loading Pyodide"
    pyodide= await loadPyodide();
    await pyodide.loadPackage("numpy");
    const src=await(await fetch("Static.py")).text();
    await pyodide.runPythonAsync(src);
    display.textContent="ready-Click Simulate";
    btn.disabled=false;
    btn.addEventListener("click",runSimulation);
}

async function runSimulation(){
    const display=document.getElementById("display-plot")
    const mode=document.getElementById("run-modes").value;




    if (mode==="One_Charge"){
     const q=Number(document.getElementById("charge").value);
    if (Number.isNaN(q)){
        display.textContent="Enter a Valid Charge";
        return;}
    pyodide.globals.set("q_js",q);
    const result=await pyodide.runPythonAsync(`one_charge(float(q_js))`);
    const data=result.toJs({dict_converter:Object.fromEntries});
    if(!data.ok){
    display.textContent=data.message||"Failed";
    return;}

    const coneTrace={

    type:"cone",
    x: data.x, y: data.y, z: data.z,
    u: data.u, v: data.v, w: data.w,
    sizemode:"scaled",
    sizeref:1,
    anchor:"tail",}

    const layout={
    scene: {aspectmode:"cube"},
    margin:{t:30}
    };


    display.textContent=`OK|One Charge|q=${q}`;
    Plotly.newPlot("plot",[coneTrace],layout);
    }




    else if (mode==="Two_Charge"){
    const q1=Number(document.getElementById("charge1").value)
    const q2=Number(document.getElementById("charge2").value)
    const l=Number(document.getElementById("distance").value)
    pyodide.globals.set("q1_js",q1);
    pyodide.globals.set("q2_js",q2);
    pyodide.globals.set("l_js",l)
    const result=await pyodide.runPythonAsync(`two_charge(float(q1_js),float(q2_js),float(l_js))`);
    const data=result.toJs({dict_converter:Object.fromEntries});
    if(!data.ok){
    display.textContent=data.message||"Failed";
    return;}

    const coneTrace={

    type:"cone",
    x: data.x, y: data.y, z: data.z,
    u: data.u, v: data.v, w: data.w,
    sizemode:"scaled",
    sizeref:1,
    anchor:"tail",}


    const layout={
    scene: {aspectmode:"cube"},
    margin:{t:30}
    };


    display.textContent=`OK|Two Charge|q1=${q1}| q2=${q2}|l=${l}`;
    Plotly.newPlot("plot",[coneTrace],layout);
    }
    else if (mode=="One_chargeGauss"){
    const q=Number(document.getElementById("chargeG").value)
    const sr=Number(document.getElementById("radius").value)
    const px=Number(document.getElementById("xcoordinate").value)
    const py=Number(document.getElementById("ycoordinate").value)
    const pz=Number(document.getElementById("zcoordinate").value)
    pyodide.globals.set("q_js",q);
    pyodide.globals.set("sr_js",sr);
    pyodide.globals.set("px_js",px)
    pyodide.globals.set("py_js",py)
    pyodide.globals.set("pz_js",pz)
    const result=await pyodide.runPythonAsync(`One_chargeGauss(float(q_js),float(sr_js),float(px_js),float(py_js),float(pz_js))`);
    const data=result.toJs({dict_converter:Object.fromEntries});
    if(!data.ok){
    display.textContent=data.message||"Failed";
    return;}

    const coneTrace={

    type:"cone",
    x: data.x, y: data.y, z: data.z,
    u: data.u, v: data.v, w: data.w,
    sizemode:"scaled",
    sizeref:1,
    anchor:"tail",}


    const layout={
    scene: {aspectmode:"cube"},
    margin:{t:30}
    };

    const sphereTrace={
    type:"scatter3d",
    x: data.Xs, y:data.Ys, z:data.Zs,
    }

    const probeTrace={
    type: "scatter3d",
    x: [data.px], y: [data.py], z: [data.pz],
    }

    display.textContent=`OK|One_chargeGauss|q=${q}| sr=${sr}|px=${px}|py=${py}|pz=${pz}|flux=${data.flux}|V=${data.V}|E=${data.Emag}`;
    Plotly.newPlot("plot",[coneTrace, sphereTrace, probeTrace],layout);
    }
    else if(mode==="Dirac_Delta"){
    const q=Number(document.getElementById("chargeD").value);
    if (Number.isNaN(q)){
        display.textContent="Enter a Valid Charge";
        return;}
    pyodide.globals.set("q_js",q);
    const result=await pyodide.runPythonAsync(`Dirac_Delta(float(q_js))`);
    const data=result.toJs({dict_converter:Object.fromEntries});
    if(!data.ok){
    display.textContent=data.message||"Failed";
    return;}

    const coneTrace={

    type:"cone",
    x: data.x, y: data.y, z: data.z,
    u: data.u, v: data.v, w: data.w,
    sizemode:"scaled",
    sizeref:1,
    anchor:"tail",}

    const layout={
    scene: {aspectmode:"cube"},
    margin:{t:30}
    };


    display.textContent=`OK|Dirac Delta|q=${q}|q_check=${data.q_check}|q=${q}|`;
    Plotly.newPlot("plot",[coneTrace],layout);

    }


    else{
    display.textContent="Coming Soon"+mode;

    }}

function updateInputs(){
    const mode=document.getElementById("run-modes").value;
    const one=document.getElementById("inputs-one");
    const two=document.getElementById("inputs-two");
    const three=document.getElementById("inputs-three");
    const four=document.getElementById("inputs-four");

    if(mode==="One_Charge"){
    one.style.display="block";
    two.style.display="none";
    three.style.display="none";
    four.style.display="none";
    } else if(mode==="Two_Charge"){
    one.style.display="none";
    two.style.display="block";
    three.style.display="none";
    four.style.display="none";
    } else if(mode==="One_chargeGauss"){
    one.style.display="none";
    two.style.display="none";
    three.style.display="block";
    four.style.display="none";
    } else if(mode==="Dirac_Delta"){
    one.style.display="none";
    two.style.display="none";
    three.style.display="none";
    four.style.display="block";
    }
    else{
    one.style.display="none";
    two.style.display="none";
    three.style.display="none";
    four.style.display="none";
    }

}
document.getElementById("run-modes").addEventListener("change",updateInputs)
updateInputs();
setup();



