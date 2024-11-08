document.addEventListener('DOMContentLoaded', async (event) => {
    const joystick = document.getElementsByClassName('joystick')[0];
    const stick = document.getElementsByClassName('stick')[0];
    // const button = document.getElementsByClassName('button')[0];
    let radius = 75;
    let dragging = false;
    let animationFrameId = null;

    const keysPressed = {};

    // Initialize WebSocket connection
    let socket = new WebSocket("ws://192.168.0.217/direction");
    /*
    socket.addEventListener("open", () => {
        socket.send("Hello Server!"); 
    });
    */
    const resetStickPosition = () => {
        stick.style.top = '75px';
        stick.style.left = '75px';
    };

    const moveStick = (x, y) => {
        stick.style.top = `${y + radius}px`;
        stick.style.left = `${x + radius}px`;

        console.log("x: " + x + ", y:" + y);
        // Send coordinates via WebSocket
        if (socket.readyState === WebSocket.OPEN) {
            socket.send(x);
            socket.send(y);
        }
    };

    const handleMovement = (clientX, clientY) => {
        const rect = joystick.getBoundingClientRect();
        let x = clientX - rect.left - 100; // Offset to center (range: -75 to 75)
        let y = clientY - rect.top - 100;

        // Constrain values between -75 and 75
        x = Math.max(-radius, Math.min(x, radius));
        y = Math.max(-radius, Math.min(y, radius));

        let current_radius = Math.sqrt(x*x + y*y); 
        if(current_radius <= radius){
            // Request a frame update to move the stick
            if (!animationFrameId) {
                animationFrameId = requestAnimationFrame(() => {
                    moveStick(x, y);
                    animationFrameId = null; // Reset after rendering
                });
            }
        }
    };

    document.addEventListener('keydown', function(event) {
        
        // Track which keys are currently pressed
        keysPressed[event.key] = true;
      
        // Check for specific key combinations
        if (keysPressed['w']) {
            if (keysPressed['a']){
                console.log("You pressed the W and A keys!");
            }
            else if (keysPressed['d']){
                console.log("You pressed the W and D keys!");
            } else {
                console.log("You pressed the W key!");
            }
        }
        else if (keysPressed['s']) {
            if (keysPressed['a']){
                console.log("You pressed the S and A keys!");
            }
            else if (keysPressed['d']){
                console.log("You pressed the S and D keys!");
            } else {
                console.log("You pressed the S key!");
            }
        }
        else if (keysPressed['a']){
            console.log("You pressed the A key!");
        }
        else if (keysPressed['d']){
            console.log("You pressed the D key!");
        }
        if (keysPressed['i']) {
            console.log('You pressed the I key!');
          // Do something else
        }
        else if (keysPressed['o']) {
            console.log('You pressed the O key!');
          // Do something else
        }
      });
      
      document.addEventListener('keyup', function(event) {
        // Remove the key from the tracked keys when it is released
        //socket.send(' ');
        keysPressed[event.key] = false;
      });

    /*
    document.addEventListener('keydown', function(event) {
        if (event.key.toLowerCase() === 'w') {
            console.log('You pressed the W key!');
        } 
        else if (event.key.toLowerCase() === 'a') {
            console.log('You pressed the A key!');
        }
        else if (event.key.toLowerCase() === 's') {
            console.log('You pressed the S key!');
        } 
        else if (event.key.toLowerCase() === 'd') {
            console.log('You pressed the D key!');
        } 
        else if (event.key.toLowerCase() === 'i') {
            console.log('You pressed the I key!');
        } 
        else if (event.key.toLowerCase() === 'o') {
            console.log('You pressed the O key!');
        } 
        
        else {
            return;
        }
        socket.send(event.key);
        if (event.repeat){
            if (event.key.toLowerCase() === 'w') {
                console.log('You pressed the W key!');
            } 
            else if (event.key.toLowerCase() === 'a') {
                console.log('You pressed the A key!');
            } 
            else if (event.key.toLowerCase() === 's') {
                console.log('You pressed the S key!');
            } 
            else if (event.key.toLowerCase() === 'd') {
                console.log('You pressed the D key!');
            } 
            else if (event.key.toLowerCase() === 'i') {
                console.log('You pressed the I key!');
            } 
            else if (event.key.toLowerCase() === 'o') {
                console.log('You pressed the O key!');
            } 
            else {
                return;
            }
            socket.send(event.key);
        }
    });
    */

    stick.addEventListener('mousedown', (e)=>{
         dragging = true;
    })
    // 2. Disable dragging of joystick when mousedown/touchdown
    document.addEventListener('mouseup', ()=>{
        if(dragging){
            dragging = false;
            resetStickPosition();
        }
    })
    // 3. Update joystick position when mousemove/touchmove
    document.addEventListener('mousemove', (e)=>{
        if(dragging){
            handleMovement(e.clientX, e.clientY);
        }
    })
});
//testing vin