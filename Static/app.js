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
    display.textContent="Ready-click simulate";
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


    display.textContent=`One charge field/Charge= ${q} Coulombs`;
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


    display.textContent=`Two Charge Field/ First charge= ${q1} Coulombs, Second Charge= ${q2} Coulombs, distance= ${l} Meters`;
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
    mode:"markers",
    marker:{size: 2, color:"cyan",opacity:0.35},
    name:"Gaussian Sphere",
    type:"scatter3d",
    x: data.Xs, y:data.Ys, z:data.Zs
    }

    const probeTrace={
    type: "scatter3d",
    mode:"markers",
    marker:{size: 8, color:"lime"},
    name:"Probe",
    x: [data.px], y: [data.py], z: [data.pz]
    }

    const centerTrace={

    type:"scatter3d",
    mode:"markers",
    marker:{size: 10,color:"red"},
    name:"Charge",
    x:[0],y:[0],z:[0]
    }

    display.textContent=`Charge= ${q} Coulombs, Gaussian Surface/ Sphere radius = ${sr} meters, probe coordinate= (${px},${py},${pz}), flux through sphere = ${data.flux} Newton-Meters Squared per Coulombs,voltage = ${data.V} Volts,electric field magnitude = ${data.Emag} Newtons per Coulomb`;
    Plotly.newPlot("plot",[coneTrace, sphereTrace, probeTrace,centerTrace],layout);
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


    display.textContent=`Dirac Delta Function/ Charge = ${q} Coulombs, ∫ρ dV ≈ ${data.q_check} C`;
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



