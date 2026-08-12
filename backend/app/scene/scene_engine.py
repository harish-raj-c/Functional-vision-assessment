import random
from typing import List
from app.models.assessment import (
    SceneConfig, ObjectConfig, ObjectType, SceneType, Level
)

class SceneEngine:
    def __init__(self):
        self.scenes = list(SceneType)
        self.objects = list(ObjectType)
        self.last_task = None

    def generate_scene(self, level: Level) -> SceneConfig:
        """Generate a scene configuration based on difficulty level"""
        scene_type = random.choice(self.scenes)
        
        if level == Level.ONE:
            return self._generate_level_one(scene_type)
        elif level == Level.TWO:
            return self._generate_level_two(scene_type)
        elif level == Level.THREE:
            return self._generate_level_three(scene_type)
        elif level == Level.FOUR:
            return self._generate_level_four(scene_type)
        else:
            return self._generate_level_five(scene_type)

    def _generate_level_one(self, scene_type: SceneType) -> SceneConfig:
        """Baseline Detection: 4-5 large objects, plain background"""
        target_object = self._get_random_target()
        target_count = random.randint(4, 5)
        
        objects = []
        for i in range(target_count):
            obj = ObjectConfig(
                type=target_object,
                x=random.uniform(0.2, 0.8),
                y=random.uniform(0.2, 0.8),
                scale=random.uniform(0.8, 1.0),  # Large
                rotation=random.uniform(0, 360),
                color=self._get_bright_color()
            )
            objects.append(obj)
        
        return SceneConfig(
            scene_type=scene_type,
            objects=objects,
            target_object=target_object,
            target_count=target_count,
            task_description=f"How many {target_object.value.replace('_', ' ')}s do you see?",
            level=Level.ONE,
            time_limit_seconds=0  # Unlimited
        )

    def _generate_level_two(self, scene_type: SceneType) -> SceneConfig:
        """Recognition: 6-8 medium objects, multiple types, small distractions"""
        target_object = self._get_random_target()
        target_count = random.randint(2, 4)
        distractor_count = random.randint(4, 5)
        
        objects = []
        # Add target objects
        for i in range(target_count):
            obj = ObjectConfig(
                type=target_object,
                x=random.uniform(0.15, 0.85),
                y=random.uniform(0.15, 0.85),
                scale=random.uniform(0.6, 0.8),  # Medium
                rotation=random.uniform(0, 360),
                color=self._get_bright_color()
            )
            objects.append(obj)
        
        # Add distractors
        for i in range(distractor_count):
            distractor = self._get_distractor(target_object)
            obj = ObjectConfig(
                type=distractor,
                x=random.uniform(0.15, 0.85),
                y=random.uniform(0.15, 0.85),
                scale=random.uniform(0.5, 0.7),
                rotation=random.uniform(0, 360),
                color=self._get_bright_color()
            )
            objects.append(obj)
        
        return SceneConfig(
            scene_type=scene_type,
            objects=objects,
            target_object=target_object,
            target_count=target_count,
            task_description=f"How many {target_object.value.replace('_', ' ')}s do you see?",
            level=Level.TWO,
            time_limit_seconds=10
        )

    def _generate_level_three(self, sceneType: SceneType) -> SceneConfig:
        """Visual Search: 10-12 objects, natural scene, moderate clutter"""
        target_object = self._get_random_target()
        target_count = random.randint(3, 5)
        total_objects = random.randint(10, 12)
        
        objects = []
        # Add target objects
        for i in range(target_count):
            obj = ObjectConfig(
                type=target_object,
                x=random.uniform(0.1, 0.9),
                y=random.uniform(0.1, 0.9),
                scale=random.uniform(0.5, 0.7),
                rotation=random.uniform(0, 360),
                color=self._get_color()
            )
            objects.append(obj)
        
        # Add distractors
        for i in range(total_objects - target_count):
            distractor = self._get_distractor(target_object)
            obj = ObjectConfig(
                type=distractor,
                x=random.uniform(0.1, 0.9),
                y=random.uniform(0.1, 0.9),
                scale=random.uniform(0.4, 0.6),
                rotation=random.uniform(0, 360),
                color=self._get_color()
            )
            objects.append(obj)
        
        return SceneConfig(
            scene_type=sceneType,
            objects=objects,
            target_object=target_object,
            target_count=target_count,
            task_description=f"How many {target_object.value.replace('_', ' ')}s do you see?",
            level=Level.THREE,
            time_limit_seconds=8
        )

    def _generate_level_four(self, scene_type: SceneType) -> SceneConfig:
        """Functional Vision: 12-15 objects, similar colors, lower contrast, peripheral"""
        target_object = self._get_random_target()
        target_count = random.randint(4, 6)
        total_objects = random.randint(12, 15)
        
        # Use similar colors for lower contrast
        base_color = self._get_color()
        
        objects = []
        # Add target objects (some in peripheral)
        for i in range(target_count):
            is_peripheral = i < 2  # First 2 in peripheral
            if is_peripheral:
                x = random.choice([random.uniform(0.05, 0.15), random.uniform(0.85, 0.95)])
                y = random.uniform(0.1, 0.9)
            else:
                x = random.uniform(0.2, 0.8)
                y = random.uniform(0.2, 0.8)
            
            obj = ObjectConfig(
                type=target_object,
                x=x,
                y=y,
                scale=random.uniform(0.4, 0.6),
                rotation=random.uniform(0, 360),
                color=base_color
            )
            objects.append(obj)
        
        # Add distractors with similar colors
        for i in range(total_objects - target_count):
            distractor = self._get_distractor(target_object)
            obj = ObjectConfig(
                type=distractor,
                x=random.uniform(0.1, 0.9),
                y=random.uniform(0.1, 0.9),
                scale=random.uniform(0.3, 0.5),
                rotation=random.uniform(0, 360),
                color=self._get_similar_color(base_color)
            )
            objects.append(obj)
        
        return SceneConfig(
            scene_type=scene_type,
            objects=objects,
            target_object=target_object,
            target_count=target_count,
            task_description=f"How many {target_object.value.replace('_', ' ')}s do you see?",
            level=Level.FOUR,
            time_limit_seconds=6
        )

    def _generate_level_five(self, scene_type: SceneType) -> SceneConfig:
        """Advanced: 15-18 objects, realistic, small, cluttered, low contrast, peripheral"""
        target_object = self._get_random_target()
        target_count = random.randint(5, 7)
        total_objects = random.randint(15, 18)
        
        base_color = self._get_muted_color()
        
        objects = []
        # Add target objects
        for i in range(target_count):
            is_peripheral = i < 3
            if is_peripheral:
                x = random.choice([random.uniform(0.02, 0.12), random.uniform(0.88, 0.98)])
                y = random.uniform(0.05, 0.95)
            else:
                x = random.uniform(0.15, 0.85)
                y = random.uniform(0.15, 0.85)
            
            obj = ObjectConfig(
                type=target_object,
                x=x,
                y=y,
                scale=random.uniform(0.25, 0.45),  # Small
                rotation=random.uniform(0, 360),
                color=base_color
            )
            objects.append(obj)
        
        # Add distractors
        for i in range(total_objects - target_count):
            distractor = self._get_distractor(target_object)
            obj = ObjectConfig(
                type=distractor,
                x=random.uniform(0.05, 0.95),
                y=random.uniform(0.05, 0.95),
                scale=random.uniform(0.2, 0.4),
                rotation=random.uniform(0, 360),
                color=self._get_muted_color()
            )
            objects.append(obj)
        
        return SceneConfig(
            scene_type=scene_type,
            objects=objects,
            target_object=target_object,
            target_count=target_count,
            task_description=f"How many {target_object.value.replace('_', ' ')}s do you see?",
            level=Level.FIVE,
            time_limit_seconds=5
        )

    def _get_random_target(self) -> ObjectType:
        """Get a random target object, avoiding repetition"""
        available = [obj for obj in self.objects if obj != self.last_task]
        target = random.choice(available)
        self.last_task = target
        return target

    def _get_distractor(self, target: ObjectType) -> ObjectType:
        """Get a random distractor object"""
        available = [obj for obj in self.objects if obj != target]
        return random.choice(available)

    def _get_bright_color(self) -> str:
        """Get a bright, high-contrast color"""
        colors = ["#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4", "#FFEAA7", "#DDA0DD", "#98D8C8"]
        return random.choice(colors)

    def _get_color(self) -> str:
        """Get a random color"""
        colors = ["#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4", "#FFEAA7", "#DDA0DD", "#98D8C8", 
                  "#F7DC6F", "#BB8FCE", "#85C1E9", "#F8B500", "#00CED1"]
        return random.choice(colors)

    def _get_similar_color(self, base_color: str) -> str:
        """Get a color similar to the base color for lower contrast"""
        # Simplified: return a muted version
        muted_colors = ["#AABAAA", "#BBAACC", "#AABBCC", "#CCAABB", "#BBCCAA"]
        return random.choice(muted_colors)

    def _get_muted_color(self) -> str:
        """Get a muted, low-contrast color"""
        colors = ["#8B8B8B", "#A0A0A0", "#909090", "#7A7A7A", "#6B6B6B", "#5C5C5C"]
        return random.choice(colors)
