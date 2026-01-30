#!/bin/bash
# Opera Control Script
# Manage Opera backend and frontend services

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

BACKEND_PLIST="com.opera.backend.plist"
FRONTEND_PLIST="com.opera.frontend.plist"
LAUNCHD_DIR="$HOME/Library/LaunchAgents"
PROJECT_DIR="/Users/sandeeplingam/VibeCoding/Opera"

# Create logs directory if it doesn't exist
mkdir -p "$PROJECT_DIR/logs"

function print_status() {
    echo -e "${BLUE}=== Opera Service Status ===${NC}"
    
    # Check backend
    if launchctl list | grep -q "com.opera.backend"; then
        echo -e "${GREEN}✓${NC} Backend: Running"
        if lsof -i :8000 > /dev/null 2>&1; then
            echo -e "  Port 8000: ${GREEN}Active${NC}"
        else
            echo -e "  Port 8000: ${RED}Not listening${NC}"
        fi
    else
        echo -e "${RED}✗${NC} Backend: Stopped"
    fi
    
    # Check frontend
    if launchctl list | grep -q "com.opera.frontend"; then
        echo -e "${GREEN}✓${NC} Frontend: Running"
        if lsof -i :3000 > /dev/null 2>&1; then
            echo -e "  Port 3000: ${GREEN}Active${NC}"
        else
            echo -e "  Port 3000: ${RED}Not listening${NC}"
        fi
    else
        echo -e "${RED}✗${NC} Frontend: Stopped"
    fi
    echo ""
}

function install_services() {
    echo -e "${BLUE}Installing Opera services...${NC}"
    
    # Copy plist files to LaunchAgents
    cp "$PROJECT_DIR/$BACKEND_PLIST" "$LAUNCHD_DIR/"
    cp "$PROJECT_DIR/$FRONTEND_PLIST" "$LAUNCHD_DIR/"
    
    echo -e "${GREEN}✓${NC} Service files installed"
    echo -e "${YELLOW}Note: Services will auto-start on next login${NC}"
}

function start_services() {
    echo -e "${BLUE}Starting Opera services...${NC}"
    
    # Load backend
    launchctl load "$LAUNCHD_DIR/$BACKEND_PLIST" 2>/dev/null || echo "Backend already loaded"
    echo -e "${GREEN}✓${NC} Backend started"
    
    # Load frontend
    launchctl load "$LAUNCHD_DIR/$FRONTEND_PLIST" 2>/dev/null || echo "Frontend already loaded"
    echo -e "${GREEN}✓${NC} Frontend started"
    
    sleep 3
    print_status
}

function stop_services() {
    echo -e "${BLUE}Stopping Opera services...${NC}"
    
    # Unload backend
    launchctl unload "$LAUNCHD_DIR/$BACKEND_PLIST" 2>/dev/null || echo "Backend not loaded"
    echo -e "${YELLOW}Backend stopped${NC}"
    
    # Unload frontend
    launchctl unload "$LAUNCHD_DIR/$FRONTEND_PLIST" 2>/dev/null || echo "Frontend not loaded"
    echo -e "${YELLOW}Frontend stopped${NC}"
}

function restart_services() {
    stop_services
    sleep 2
    start_services
}

function uninstall_services() {
    echo -e "${BLUE}Uninstalling Opera services...${NC}"
    
    stop_services
    
    # Remove plist files
    rm -f "$LAUNCHD_DIR/$BACKEND_PLIST"
    rm -f "$LAUNCHD_DIR/$FRONTEND_PLIST"
    
    echo -e "${GREEN}✓${NC} Services uninstalled"
}

function show_logs() {
    echo -e "${BLUE}=== Recent Backend Logs ===${NC}"
    tail -n 20 "$PROJECT_DIR/logs/backend.log" 2>/dev/null || echo "No backend logs yet"
    
    echo ""
    echo -e "${BLUE}=== Recent Frontend Logs ===${NC}"
    tail -n 20 "$PROJECT_DIR/logs/frontend.log" 2>/dev/null || echo "No frontend logs yet"
}

function show_help() {
    cat << EOF
${BLUE}Opera Control Script${NC}

Usage: ./opera-control.sh [command]

Commands:
  ${GREEN}install${NC}   - Install services (one-time setup)
  ${GREEN}start${NC}     - Start Opera services
  ${GREEN}stop${NC}      - Stop Opera services
  ${GREEN}restart${NC}   - Restart Opera services
  ${GREEN}status${NC}    - Show service status
  ${GREEN}logs${NC}      - Show recent logs
  ${GREEN}uninstall${NC} - Remove services completely
  ${GREEN}help${NC}      - Show this help message

Examples:
  ./opera-control.sh install    # First time setup
  ./opera-control.sh start      # Start Opera
  ./opera-control.sh status     # Check if running

EOF
}

# Main command handler
case "${1:-status}" in
    install)
        install_services
        ;;
    start)
        start_services
        ;;
    stop)
        stop_services
        ;;
    restart)
        restart_services
        ;;
    status)
        print_status
        ;;
    logs)
        show_logs
        ;;
    uninstall)
        uninstall_services
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo -e "${RED}Unknown command: $1${NC}"
        show_help
        exit 1
        ;;
esac
