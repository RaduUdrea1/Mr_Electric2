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
    document.getElementById("charge").addEventListener("input",(e)=>{
        document.getElementById("charge-val").textContent=e.target.value;
        throttledRun();

    });

    document.getElementById("charge1").addEventListener("input",(e)=>{
        document.getElementById("charge-val1").textContent=e.target.value;
        throttledRun();

    });

    document.getElementById("charge2").addEventListener("input",(e)=>{
        document.getElementById("charge-val2").textContent=e.target.value;
        throttledRun();

    });

    document.getElementById("chargeG").addEventListener("input",(e)=>{
        document.getElementById("charge-valg").textContent=e.target.value;
        throttledRun();

    });
}
function throttle(fn, wait) {
  let last = 0;
  return function (...args) {
    const now = Date.now();
    if (now - last >= wait) {
      last = now;
      return fn.apply(this, args);
    }
  };
}
const throttledRun=throttle(runSimulation,150);
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



const layout = {
  scene: {
    aspectmode: "cube",
    xaxis: { range: [-100, 100] },
    yaxis: { range: [-100, 100] },
    zaxis: { range: [-100, 100] },
  },
  margin: { t: 30 },
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
    const x=Number(document.getElementById("locationx").value)
    const y=Number(document.getElementById("locationy").value)
    const z=Number(document.getElementById("locationz").value)


    if (Number.isNaN(q)){
        display.textContent="Enter a Valid Charge";
        return;}
    if (Number.isNaN(x)||Number.isNaN(y)||Number.isNaN(z)){
        display.textContent="Enter a valid location";
        return;}
    if(Number.isNaN(px)||Number.isNaN(py)||Number.isNaN(pz)){
        display.textContent="Enter Valid Probe Points";
        return;}
    pyodide.globals.set("q_js",q);
    pyodide.globals.set("px_js",px);
    pyodide.globals.set("py_js",py);
    pyodide.globals.set("pz_js",pz);
    pyodide.globals.set("x_js",x)
    pyodide.globals.set("y_js",y)
    pyodide.globals.set("z_js",z)

    const result=await pyodide.runPythonAsync(`one_charge(float(q_js),float(x_js),float(y_js),float(z_js),float(px_js),float(py_js),float(pz_js))`);
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
    x:[data.qx],y:[data.qy],z:[data.qz]
    }



    display.textContent=`One charge field/Charge= ${q} nanocoulombs, total electric field magnitude at probe=${data.Emag} N/C, E as components= (${data.Ex}, ${data.Ey}, ${data.Ez}) N/C, Potential at probe=${data.V} volts`;
    plotCones(data, [probeTrace,centerTrace]);
    }




    else if (mode==="Two_Charge"){
    const q1=Number(document.getElementById("charge1").value)
    const q2=Number(document.getElementById("charge2").value)
    const x1=Number(document.getElementById("locationx1").value)
    const y1=Number(document.getElementById("locationy1").value)
    const z1=Number(document.getElementById("locationz1").value)
    const x2=Number(document.getElementById("locationx2").value)
    const y2=Number(document.getElementById("locationy2").value)
    const z2=Number(document.getElementById("locationz2").value)
    const px=Number(document.getElementById("xcoordinate2").value)
    const py=Number(document.getElementById("ycoordinate2").value)
    const pz=Number(document.getElementById("zcoordinate2").value)
    const totalDist=Math.sqrt((x2-x1)**2+(y2-y1)**2+(z2-z1)**2)
    if (Number.isNaN(q1)||Number.isNaN(q2)){
        display.textContent="Enter a Valid Charge";
        return;
    }
    if (!(totalDist>0)||Number.isNaN(x1)||Number.isNaN(y1)||Number.isNaN(z1)||Number.isNaN(x2)||Number.isNaN(y2)||Number.isNaN(z2)){
        display.textContent="Enter a Valid Location";
        return;
    }
    if(Number.isNaN(px)||Number.isNaN(py)||Number.isNaN(pz)){
        display.textContent="Enter Valid Probe Points";
        return;}
    pyodide.globals.set("q1_js",q1);
    pyodide.globals.set("q2_js",q2);
    pyodide.globals.set("x1_js",x1);
    pyodide.globals.set("y1_js",y1);
    pyodide.globals.set("z1_js",z1);
    pyodide.globals.set("x2_js",x2);
    pyodide.globals.set("y2_js",y2);
    pyodide.globals.set("z2_js",z2);
    pyodide.globals.set("px_js",px);
    pyodide.globals.set("py_js",py);
    pyodide.globals.set("pz_js",pz);
    const result=await pyodide.runPythonAsync(`two_charge(float(q1_js),float(q2_js),float(px_js),float(py_js),float(pz_js), float(x1_js),float(y1_js),float(z1_js), float(x2_js),float(y2_js),float(z2_js))`);
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
    x:[data.x1],y:[data.y1],z:[data.z1]
    }
    const center2Trace={
    type:"scatter3d",
    mode:"markers",
    marker:{size: 5,color:"red"},
    name:"Charge",
    x:[data.x2],y:[data.y2],z:[data.z2]
    }


    display.textContent=`Two Charge Field/ First charge= ${q1} nanocoulombs, Second Charge= ${q2} nanocoulombs, distance= ${data.totalDist} meters, total electric field magnitude at probe=${data.Emag} N/C, E as components= (${data.Ex}, ${data.Ey}, ${data.Ez}) N/C, Potential at probe=${data.V} volts, Potential Energy at probe=${data.U} joules`;
    plotCones(data,[probeTrace,center1Trace,center2Trace]);
    }
    else if (mode=="One_chargeGauss"){
    const q=Number(document.getElementById("chargeG").value)
    const sr=Number(document.getElementById("radius").value)
    const px=Number(document.getElementById("xcoordinate3").value)
    const py=Number(document.getElementById("ycoordinate3").value)
    const pz=Number(document.getElementById("zcoordinate3").value)
    const x=Number(document.getElementById("locationxg").value)
    const y=Number(document.getElementById("locationyg").value)
    const z=Number(document.getElementById("locationzg").value)
    if (Number.isNaN(q)){
        display.textContent="Enter a Valid Charge";
        return;}
    if (Number.isNaN(sr)||sr<=0){
        display.textContent="Enter a Valid Radius";
        return;}
    if(Number.isNaN(px)||Number.isNaN(py)||Number.isNaN(pz)||Number.isNaN(x)||Number.isNaN(y)||Number.isNaN(z)){
        display.textContent="Enter Valid Points";
        return;}
    pyodide.globals.set("q_js",q);
    pyodide.globals.set("sr_js",sr);
    pyodide.globals.set("px_js",px)
    pyodide.globals.set("py_js",py)
    pyodide.globals.set("pz_js",pz)
    pyodide.globals.set("x_js",x)
    pyodide.globals.set("y_js",y)
    pyodide.globals.set("z_js",z)
    const result=await pyodide.runPythonAsync(`One_chargeGauss(float(q_js), float(x_js),float(y_js),float(z_js),float(sr_js),float(px_js),float(py_js),float(pz_js))`);
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
    x:[data.qx],y:[data.qy],z:[data.qz]
    }

    display.textContent=`Charge= ${q} nanocoulombs, Gaussian Surface/ Sphere radius = ${sr} meters, probe coordinate= (${px},${py},${pz}),total electric field magnitude at probe=${data.Emag} N/C, ${data.inside? "INSIDE":"OUTSIDE"}, flux through sphere = ${data.flux} N*m^2/C,voltage = ${data.V} Volts, E as components= (${data.Ex}, ${data.Ey}, ${data.Ez}) N/C`;
    plotCones(data,[sphereTrace,probeTrace,centerTrace]);
    }
    else if(mode==="Charged_ring"){
    const q=Number(document.getElementById("chargeD").value);
    if (Number.isNaN(q)){
        display.textContent="Enter a Valid Charge";
        return;}
    pyodide.globals.set("q_js",q);
    const result=await pyodide.runPythonAsync(`Charged_ring(float(q_js))`);
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


    display.textContent=`Charged Ring Plot/ Charge = ${q} nanocoulombs, ∫ρ dV ≈ ${data.q_check} C`;
    plotCones(data,[centerTrace]);

    }

     else if (mode=="Vacuum_permittivity"){
    const q=Number(document.getElementById("chargep").value)
    const x=Number(document.getElementById("locationxp").value)
    const y=Number(document.getElementById("locationyp").value)
    const z=Number(document.getElementById("locationzp").value)
    const px=Number(document.getElementById("xcoordinate1p").value)
    const py=Number(document.getElementById("ycoordinate1p").value)
    const pz=Number(document.getElementById("zcoordinate1p").value)
    const m=Number(document.getElementById("permittivity").value)

    if (Number.isNaN(q)){
        display.textContent="Enter a Valid Charge";
        return;}

    if(Number.isNaN(px)||Number.isNaN(py)||Number.isNaN(pz)||Number.isNaN(x)||Number.isNaN(y)||Number.isNaN(z)){
        display.textContent="Enter Valid Points";
        return;}

    pyodide.globals.set("q_js",q);
    pyodide.globals.set("px_js",px)
    pyodide.globals.set("py_js",py)
    pyodide.globals.set("pz_js",pz)
    pyodide.globals.set("x_js",x)
    pyodide.globals.set("y_js",y)
    pyodide.globals.set("z_js",z)
    pyodide.globals.set("m_js",m)


    const result=await pyodide.runPythonAsync(`Relative_permittivity(float(q_js),float(x_js),float(y_js),float(z_js),float(px_js),float(py_js),float(pz_js),float(m_js))`);
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
    x:[data.qx],y:[data.qy],z:[data.qz]
    }



    display.textContent=`Permittivity Field/Charge= ${q} nanocoulombs, total electric field magnitude at probe=${data.Emag} N/C, E as components= (${data.Ex}, ${data.Ey}, ${data.Ez}) N/C, Potential at probe=${data.V} volts, Permittivity of space=${m}`;
    plotCones(data, [probeTrace,centerTrace]);
    }
    }




function updateInputs(){
    const mode=document.getElementById("run-modes").value;
    const one=document.getElementById("inputs-one");
    const two=document.getElementById("inputs-two");
    const three=document.getElementById("inputs-three");
    const four=document.getElementById("inputs-four");
    const five=document.getElementById("inputs-five");

    if(mode==="One_Charge"){
    one.style.display="block";
    two.style.display="none";
    three.style.display="none";
    four.style.display="none";
    five.style.display="none";
    } else if(mode==="Two_Charge"){
    one.style.display="none";
    two.style.display="block";
    three.style.display="none";
    four.style.display="none";
    five.style.display="none";
    } else if(mode==="One_chargeGauss"){
    one.style.display="none";
    two.style.display="none";
    three.style.display="block";
    four.style.display="none";
    five.style.display="none";
    } else if(mode==="Dirac_Delta"){
    one.style.display="none";
    two.style.display="none";
    three.style.display="none";
    four.style.display="block";
    five.style.display="none";
    }else if(mode==="Vacuum_permittivity"){
    one.style.display="none";
    two.style.display="none";
    three.style.display="none";
    four.style.display="none";
    five.style.display="block";
    }
    else{
    one.style.display="none";
    two.style.display="none";
    three.style.display="none";
    four.style.display="none";
    five.style.display="none";
    }




}

document.getElementById("run-modes").addEventListener("change",updateInputs)
updateInputs();
setup();



