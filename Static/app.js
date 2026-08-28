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
    display.textContent="Ready-run simulation!";
    btn.disabled=false;
    btn.addEventListener("click",runSimulation);
}
function plotCones(data,extraTraces){




 const coneTrace={

    type:"cone",
    x: data.x, y: data.y, z: data.z,
    u: data.u, v: data.v, w: data.w,
    sizemode:"absolute",
    sizeref:0.5,
    anchor:"tail",
    colorscale: [[0, "#0000FF"], [1, "#0000FF"]],
    showscale: false,
    hoverinfo: "skip",



    }



 const layout={
    scene: {aspectmode:"cube"},
    margin:{t:30}
    };

 const traces=[coneTrace];
    if(extraTraces){
    traces.push(...extraTraces);
    }


 Plotly.newPlot("plot",traces,layout);

}

async function runSimulation(){
    const display=document.getElementById("display-plot")
    const mode=document.getElementById("run-modes").value;




    if (mode==="One_Charge"){
    const q=Number(document.getElementById("charge").value);
    const px=Number(document.getElementById("xcoordinate1").value)
    const py=Number(document.getElementById("ycoordinate1").value)
    const pz=Number(document.getElementById("zcoordinate1").value)
    if (Number.isNaN(q)){
        display.textContent="Enter a Valid Charge";
        return;}
    if(Number.isNaN(px)||Number.isNaN(py)||Number.isNaN(pz)){
        display.textContent="Enter Valid Probe Points";
        return;}
    pyodide.globals.set("q_js",q);
    pyodide.globals.set("px_js",px);
    pyodide.globals.set("py_js",py);
    pyodide.globals.set("pz_js",pz);

    const result=await pyodide.runPythonAsync(`one_charge(float(q_js),float(px_js),float(py_js),float(pz_js))`);
    const data=result.toJs({dict_converter:Object.fromEntries});
    if(!data.ok){
    display.textContent=data.message||"Failed";
    return;}
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



    display.textContent=`One charge field/Charge= ${q} nanocoulombs, total electric field magnitude at probe=${data.Emag} N/C, E as components= (${data.Ex}, ${data.Ey}, ${data.Ez}) N/C`;
    plotCones(data, [probeTrace,centerTrace]);
    }




    else if (mode==="Two_Charge"){
    const q1=Number(document.getElementById("charge1").value)
    const q2=Number(document.getElementById("charge2").value)
    const l1=Number(document.getElementById("distance(x)").value)
    const l2=Number(document.getElementById("distance(y)").value)
    const l3=Number(document.getElementById("distance(z)").value)
    const px=Number(document.getElementById("xcoordinate2").value)
    const py=Number(document.getElementById("ycoordinate2").value)
    const pz=Number(document.getElementById("zcoordinate2").value)
    const totalDist=Math.sqrt(l1**2+l2**2+l3**2)
    if (Number.isNaN(q1)||Number.isNaN(q2)){
        display.textContent="Enter a Valid Charge";
        return;
    }
    if (!(totalDist>0)||Number.isNaN(l1)||Number.isNaN(l2)||Number.isNaN(l3)){
        display.textContent="Enter a Valid Length";
        return;
    }
    if(Number.isNaN(px)||Number.isNaN(py)||Number.isNaN(pz)){
        display.textContent="Enter Valid Probe Points";
        return;}
    pyodide.globals.set("q1_js",q1);
    pyodide.globals.set("q2_js",q2);
    pyodide.globals.set("l1_js",l1);
    pyodide.globals.set("l2_js",l2);
    pyodide.globals.set("l3_js",l3);
    pyodide.globals.set("px_js",px);
    pyodide.globals.set("py_js",py);
    pyodide.globals.set("pz_js",pz);
    const result=await pyodide.runPythonAsync(`two_charge(float(q1_js),float(q2_js),float(px_js),float(py_js),float(pz_js), float(l1_js),float(l2_js),float(l3_js))`);
    const data=result.toJs({dict_converter:Object.fromEntries});


    if(!data.ok){
    display.textContent=data.message||"Failed";
    return;}
    const probeTrace={
    type: "scatter3d",
    mode:"markers",
    marker:{size: 8, color:"lime"},
    name:"Probe",
    x: [data.px], y: [data.py], z: [data.pz]
    }

    const center1Trace={

    type:"scatter3d",
    mode:"markers",
    marker:{size: 5,color:"red"},
    name:"Charge",
    x:[-l1/2],y:[-l2/2],z:[-l3/2]
    }
    const center2Trace={
    type:"scatter3d",
    mode:"markers",
    marker:{size: 5,color:"red"},
    name:"Charge",
    x:[l1/2],y:[l2/2],z:[l3/2]
    }


    display.textContent=`Two Charge Field/ First charge= ${q1} nanocoulombs, Second Charge= ${q2} nanocoulombs, distance= ${data.totalDist} meters, total electric field magnitude at probe=${data.Emag} N/C, E as components= (${data.Ex}, ${data.Ey}, ${data.Ez}) N/C`;
    plotCones(data,[probeTrace,center1Trace,center2Trace]);
    }
    else if (mode=="One_chargeGauss"){
    const q=Number(document.getElementById("chargeG").value)
    const sr=Number(document.getElementById("radius").value)
    const px=Number(document.getElementById("xcoordinate3").value)
    const py=Number(document.getElementById("ycoordinate3").value)
    const pz=Number(document.getElementById("zcoordinate3").value)
    if (Number.isNaN(q)){
        display.textContent="Enter a Valid Charge";
        return;}
    if (Number.isNaN(sr)||sr<=0){
        display.textContent="Enter a Valid Radius";
        return;}
    if(Number.isNaN(px)||Number.isNaN(py)||Number.isNaN(pz)){
        display.textContent="Enter Valid Probe Points";
        return;}
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

    display.textContent=`Charge= ${q} nanocoulombs, Gaussian Surface/ Sphere radius = ${sr} meters, probe coordinate= (${px},${py},${pz}), flux through sphere = ${data.flux} N*m^2/C,voltage = ${data.V} Volts, total electric field magnitude at probe=${data.Emag} N/C, E as components= (${data.Ex}, ${data.Ey}, ${data.Ez}) N/C`;
    plotCones(data,[sphereTrace,probeTrace,centerTrace]);
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
    const centerTrace={

    type:"scatter3d",
    mode:"markers",
    marker:{size: 10,color:"red"},
    name:"Charge",
    x:[0],y:[0],z:[0]
    }


    display.textContent=`Dirac Delta Function/ Charge = ${q} nanocoulombs, ∫ρ dV ≈ ${data.q_check} C`;
    plotCones(data,[centerTrace]);

    }


    }

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



